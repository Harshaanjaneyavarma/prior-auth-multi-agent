# Multi-Agent Prior Authorization Automation

Synthetic healthcare AI workflow demo using LangGraph, FastAPI, FHIR R4-shaped fixtures, optional MCP tools, SQLite, and mandatory clinician approval.

**Educational prototype only.** Do not use real patient information. Not HIPAA-compliant, clinically validated, or suitable for production.

## Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```
API docs: http://localhost:8000/docs

## Workflow
Intake → FHIR patient lookup → fictional policy lookup → clinical rule evaluation → documentation → clinician approval interrupt → simulated payer submission.

## Demo
```bash
curl -X POST http://localhost:8000/requests -H 'Content-Type: application/json' -d '{"patient_id":"demo-patient-001","procedure_code":"70551","diagnosis_code":"G43.909","clinician_id":"demo-clinician","clinical_notes":"Synthetic note","supporting_document_ids":["demo-doc-1"]}'
```
Then call `POST /requests/{id}/decision` with header `X-Demo-Key: demo-clinician-key` and body `{"approved":true,"reviewer_id":"demo-reviewer"}`.

## Notes
MCP server is a standalone optional interface, not yet invoked by LangGraph nodes. In-memory LangGraph checkpoints do not survive restarts. SQLite stores status and metadata audit logs. Demo key is not production authentication.
