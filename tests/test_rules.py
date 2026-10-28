from app.rules import evaluate
from app.fhir import make_bundle
from app.services import get_patient,get_policy

def test_missing():
    r=evaluate({"diagnosis_code":"G43.909"},get_policy("70551"))
    assert not r.eligible_for_review
    assert "clinical_notes" in r.missing

def test_complete():
    r=evaluate({"diagnosis_code":"G43.909","clinical_notes":"Synthetic note","supporting_document_ids":["demo-doc-1"]},get_policy("70551"))
    assert r.eligible_for_review

def test_bundle():
    b=make_bundle(get_patient("demo-patient-001"),"70551","G43.909","demo-1")
    assert [x["resource"]["resourceType"] for x in b["entry"]]==["Patient","Condition","ServiceRequest"]
