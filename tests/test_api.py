from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
payload={"patient_id":"demo-patient-001","procedure_code":"70551","diagnosis_code":"G43.909","clinician_id":"demo-clinician"}

def test_approval():
    r=client.post("/requests",json=payload)
    assert r.status_code==201,r.text
    rid=r.json()["request_id"]
    done=client.post(f"/requests/{rid}/decision",json={"approved":True,"reviewer_id":"demo-reviewer"},headers={"X-Demo-Key":"demo-clinician-key"})
    assert done.status_code==200,done.text
    assert done.json()["status"]=="simulated_submission_complete"

def test_rejection():
    rid=client.post("/requests",json=payload).json()["request_id"]
    done=client.post(f"/requests/{rid}/decision",json={"approved":False,"reviewer_id":"demo-reviewer"},headers={"X-Demo-Key":"demo-clinician-key"})
    assert done.json()["status"]=="rejected_by_clinician"
