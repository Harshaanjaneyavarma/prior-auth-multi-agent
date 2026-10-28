import json,sqlite3
from datetime import datetime,timezone
from app.config import DATA_DIR

def now(): return datetime.now(timezone.utc).isoformat()

def connection():
    DATA_DIR.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(DATA_DIR/"demo.db",timeout=10)
    c.row_factory=sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.executescript("""CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY,status TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL,procedure_code TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,request_id TEXT NOT NULL,event TEXT NOT NULL,actor TEXT NOT NULL,at TEXT NOT NULL,detail TEXT NOT NULL);""")
    return c

def register(rid,code,status):
    with connection() as c:
        t=now()
        c.execute("INSERT INTO requests VALUES(?,?,?,?,?)",(rid,status,t,t,code))

def update(rid,status):
    with connection() as c: c.execute("UPDATE requests SET status=?,updated_at=? WHERE id=?",(status,now(),rid))

def audit(rid,event,actor="system",detail=None):
    with connection() as c: c.execute("INSERT INTO audit(request_id,event,actor,at,detail) VALUES(?,?,?,?,?)",(rid,event,actor,now(),json.dumps(detail or {})))

def get(rid):
    with connection() as c:
        row=c.execute("SELECT * FROM requests WHERE id=?",(rid,)).fetchone()
        return dict(row) if row else None

def list_requests(limit=50):
    with connection() as c: return [dict(x) for x in c.execute("SELECT * FROM requests ORDER BY created_at DESC LIMIT ?",(limit,))]

def audit_trail(rid):
    with connection() as c: return [dict(x) for x in c.execute("SELECT * FROM audit WHERE request_id=? ORDER BY id",(rid,))]

def stats():
    with connection() as c: return {x["status"]:x["n"] for x in c.execute("SELECT status,COUNT(*) AS n FROM requests GROUP BY status")}
