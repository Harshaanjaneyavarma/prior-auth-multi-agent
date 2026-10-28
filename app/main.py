from uuid import uuid4
from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel,Field
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from app.workflow import build_graph
from app.security import reviewer
from app import storage
from app.services import get_patient,get_policy

app=FastAPI(title="Multi-Agent Prior Authorization Demo",version="1.0.0",description="Synthetic fixtures only; not for clinical use.")
workflow=build_graph(MemorySaver())

class Request(BaseModel):
    patient_id:str=Field(min_length=1,max_length=80)
    procedure_code:str=Field(min_length=1,max_length=32)
    diagnosis_code:str=Field(min_length=1,max_length=32)
    clinician_id:str=Field(min_length=1,max_length=80)
    clinical_notes:str=Field(default="",max_length=3000)
    supporting_document_ids:list[str]=Field(default_factory=list,max_length=20)

class Decision(BaseModel):
    approved:bool
    reviewer_id:str=Field(min_length=1,max_length=80)

def config(rid): return {"configurable":{"thread_id":rid}}

def present(result,rid):
    if "__interrupt__" in result: return {"request_id":rid,"status":"awaiting_clinician_approval","review":result["__interrupt__"][0].value}
    return {"request_id":rid,"status":result.get("status","unknown"),"packet":result.get("packet"),"submission":result.get("submission")}

@app.post("/requests",status_code=201)
def create_request(request:Request):
    rid=str(uuid4())
    try:
        payload=request.model_dump()
        payload["request_id"]=rid
        result=workflow.invoke({"request":payload},config=config(rid))
    except ValueError as e: raise HTTPException(422,str(e)) from e
    response=present(result,rid)
    storage.register(rid,request.procedure_code,response["status"])
    storage.audit(rid,"created",detail={"procedure_code":request.procedure_code})
    return response

@app.post("/requests/{request_id}/decision")
def decide(request_id:str,decision:Decision,actor:str=Depends(reviewer)):
    if not storage.get(request_id): raise HTTPException(404,"Request not found")
    state=workflow.get_state(config(request_id))
    if not state.interrupts: raise HTTPException(409,"Request not awaiting approval (or server restarted)")
    if decision.reviewer_id!=actor: raise HTTPException(403,"Reviewer mismatch")
    result=workflow.invoke(Command(resume=decision.model_dump()),config=config(request_id))
    response=present(result,request_id)
    storage.update(request_id,response["status"])
    storage.audit(request_id,"clinician_approved" if decision.approved else "clinician_rejected",actor)
    if response.get("submission"): storage.audit(request_id,"mock_payer_submission",actor,{"submission_id":response["submission"]["submission_id"]})
    return response

@app.get("/requests")
def list_requests(actor:str=Depends(reviewer),limit:int=20): return storage.list_requests(max(1,min(limit,100)))

@app.get("/requests/{request_id}")
def get_request(request_id:str,actor:str=Depends(reviewer)):
    row=storage.get(request_id)
    if not row: raise HTTPException(404,"Request not found")
    return row

@app.get("/requests/{request_id}/audit")
def audit(request_id:str,actor:str=Depends(reviewer)):
    if not storage.get(request_id): raise HTTPException(404,"Request not found")
    return storage.audit_trail(request_id)

@app.get("/metrics")
def metrics(actor:str=Depends(reviewer)): return {"status_counts":storage.stats()}

@app.get("/fhir/Patient/{patient_id}")
def patient(patient_id:str,actor:str=Depends(reviewer)):
    try: return get_patient(patient_id)
    except ValueError as e: raise HTTPException(404,str(e)) from e

@app.get("/policies/{procedure_code}")
def policy(procedure_code:str,actor:str=Depends(reviewer)):
    try: return get_policy(procedure_code)
    except ValueError as e: raise HTTPException(404,str(e)) from e

@app.get("/health")
def health(): return {"status":"ok","synthetic_data_only":True,"production_ready":False}
