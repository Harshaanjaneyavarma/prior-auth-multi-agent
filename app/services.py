import json
from app.config import BASE_DIR

def get_patient(patient_id):
    for patient in json.loads((BASE_DIR/"data/patients.json").read_text()):
        if patient["id"]==patient_id: return patient
    raise ValueError("Synthetic patient not found")

def get_policy(procedure_code):
    policies=json.loads((BASE_DIR/"data/policies.json").read_text())
    if procedure_code not in policies: raise ValueError("Unsupported fictional procedure code")
    return policies[procedure_code]
