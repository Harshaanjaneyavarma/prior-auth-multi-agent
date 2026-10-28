from fastapi import Header,HTTPException
from app.config import API_KEYS

def reviewer(x_demo_key: str | None=Header(default=None)):
    if not x_demo_key or x_demo_key not in API_KEYS: raise HTTPException(401,"Valid demo reviewer key required")
    return "demo-reviewer"
