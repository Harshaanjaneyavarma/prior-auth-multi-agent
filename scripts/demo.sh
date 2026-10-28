#!/usr/bin/env bash
set -euo pipefail
curl -s -X POST http://localhost:8000/requests -H 'Content-Type: application/json' -d '{"patient_id":"demo-patient-001","procedure_code":"70551","diagnosis_code":"G43.909","clinician_id":"demo-clinician","clinical_notes":"Synthetic note","supporting_document_ids":["demo-doc-1"]}'
echo
