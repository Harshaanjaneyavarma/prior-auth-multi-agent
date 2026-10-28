from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.types import interrupt
from app.services import get_patient,get_policy
from app.rules import evaluate
from app.fhir import make_bundle
from app.payer import submit

class AuthState(TypedDict,total=False):
    request:dict
    patient:dict
    policy:dict
    rule_result:dict
    packet:dict
    findings:list[str]
    approved:bool
    reviewer_id:str
    status:str
    submission:dict

def intake(s): return {"findings":["Synthetic intake validated"]}
def fhir_agent(s): return {"patient":get_patient(s["request"]["patient_id"])}
def policy_agent(s): return {"policy":get_policy(s["request"]["procedure_code"])}

def clinical_agent(s):
    r=evaluate(s["request"],s["policy"])
    return {"rule_result":{"eligible_for_review":r.eligible_for_review,"missing":r.missing,"findings":r.findings},"findings":s["findings"]+r.findings}

def documentation_agent(s):
    r=s["request"]
    return {"packet":{"request":r,"fhir_bundle":make_bundle(s["patient"],r["procedure_code"],r["diagnosis_code"],r["request_id"]),"policy_name":s["policy"]["name"],"rule_result":s["rule_result"],"findings":s["findings"]}}

def approval_agent(s):
    d=interrupt({"type":"clinician_approval_required","rule_result":s["rule_result"],"packet":s["packet"]})
    if not isinstance(d,dict) or not isinstance(d.get("approved"),bool) or not d.get("reviewer_id"):
        raise ValueError("Explicit clinician decision required")
    return {"approved":d["approved"],"reviewer_id":d["reviewer_id"],"status":"approved_for_demo_submission" if d["approved"] else "rejected_by_clinician"}

def submission_agent(s):
    return {"submission":submit(s["packet"],s["reviewer_id"]),"status":"simulated_submission_complete"}

def build_graph(checkpointer):
    g=StateGraph(AuthState)
    for name,fn in [("intake",intake),("fhir",fhir_agent),("policy",policy_agent),("clinical",clinical_agent),("documentation",documentation_agent),("approval",approval_agent),("submit",submission_agent)]:
        g.add_node(name,fn)
    g.add_edge(START,"intake")
    for a,b in [("intake","fhir"),("fhir","policy"),("policy","clinical"),("clinical","documentation"),("documentation","approval")]: g.add_edge(a,b)
    g.add_conditional_edges("approval",lambda s:"submit" if s["approved"] else "end",{"submit":"submit","end":END})
    g.add_edge("submit",END)
    return g.compile(checkpointer=checkpointer)
