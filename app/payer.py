from datetime import datetime,timezone
from uuid import uuid4

def submit(packet,reviewer_id):
    if not reviewer_id: raise ValueError("Reviewer required")
    return {"submission_id":"SIM-"+uuid4().hex[:12].upper(),"status":"received_by_mock_payer","submitted_at":datetime.now(timezone.utc).isoformat(),"destination":"local-simulator","reviewer_id":reviewer_id}
