def make_bundle(patient,procedure_code,diagnosis_code,request_id):
    condition={"resourceType":"Condition","id":"condition-"+request_id,"subject":{"reference":"Patient/"+patient["id"]},"code":{"coding":[{"system":"http://hl7.org/fhir/sid/icd-10-cm","code":diagnosis_code}]}}
    service={"resourceType":"ServiceRequest","id":request_id,"status":"draft","intent":"order","subject":{"reference":"Patient/"+patient["id"]},"code":{"coding":[{"system":"http://www.ama-assn.org/go/cpt","code":procedure_code}]}}
    return {"resourceType":"Bundle","type":"collection","entry":[{"resource":r} for r in (patient,condition,service)]}
