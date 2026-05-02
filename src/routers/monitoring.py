from fastapi import APIRouter, Depends, HTTPException, Header
from jose import jwt, JWTError
from datetime import timedelta
import os

from ..auth import create_token, SECRET_KEY
from ..dependencies import require_role

router = APIRouter()

MONITORING_API_KEY = os.getenv("MONITORING_API_KEY", "supersecret123")
'''
@router.post("/token")
def monitoring_token(key: str,
                     user=Depends(require_role(["monitoring_officer"]))):
    if key != MONITORING_API_KEY:
        raise HTTPException(401, "Invalid key")

    return {"token": create_token({"role": "monitoring_officer"}, expires=1)}


@router.get("/attendance")
def monitoring(token: str = Header(...)):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if data["role"] != "monitoring_officer":
            raise HTTPException(401)
    except:
        raise HTTPException(401)

    return {"data": "read-only attendance"}

'''

from datetime import datetime, timedelta, timezone

@router.post("/token")
def generate_monitoring_token(key: str, token: str = Header(...)):
    # verify API key
    if key != os.getenv("MONITORING_API_KEY", "supersecret123"):
        raise HTTPException(status_code=401, detail="Invalid API key")

    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    if payload.get("role") != "monitoring_officer":
        raise HTTPException(status_code=403, detail="Forbidden")

    # ✅ Create scoped token
    monitoring_token = jwt.encode({
        "scope": "monitoring",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return {"monitoring_token": monitoring_token}

SECRET_KEY = os.getenv("SECRET_KEY", "secret")

@router.get("/attendance")
def get_attendance(token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 🔥 CRITICAL CHECK
    if payload.get("scope") != "monitoring":
        raise HTTPException(status_code=401, detail="Invalid monitoring token")

    return {"data": "read-only attendance"}

@router.post("/attendance")
def block():
    raise HTTPException(405, "Method Not Allowed")