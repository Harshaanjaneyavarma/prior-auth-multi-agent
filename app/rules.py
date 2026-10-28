from dataclasses import dataclass

@dataclass
class RuleResult:
    eligible_for_review: bool
    missing: list[str]
    findings: list[str]

def evaluate(request,policy):
    missing=[]
    if not request.get("clinical_notes"): missing.append("clinical_notes")
    if not request.get("supporting_document_ids"): missing.append("supporting_document_ids")
    supported=request.get("diagnosis_code") in policy["supported_diagnoses"]
    return RuleResult(not missing and supported,missing,["Fictional diagnosis policy match" if supported else "Fictional diagnosis policy mismatch"])
