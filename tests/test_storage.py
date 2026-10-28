from app import storage

def test_storage(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,"DATA_DIR",tmp_path)
    storage.register("demo","70551","awaiting_clinician_approval")
    storage.audit("demo","created")
    assert storage.get("demo")["status"]=="awaiting_clinician_approval"
    assert storage.audit_trail("demo")[0]["event"]=="created"
    storage.update("demo","rejected_by_clinician")
    assert storage.stats()["rejected_by_clinician"]==1
