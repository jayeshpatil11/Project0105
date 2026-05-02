from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
import uuid

from ..dependencies import require_role
from ..database import SessionLocal
from ..models import Batch, BatchInvite, BatchStudent

router = APIRouter()

@router.post("/")
def create_batch(name: str, user=Depends(require_role(["trainer","institution"]))):
    db = SessionLocal()
    batch = Batch(name=name, institution_id=1)
    db.add(batch)
    db.commit()
    return {"batch_id": batch.id}


@router.post("/{batch_id}/invite")
def invite(batch_id: int, user=Depends(require_role(["trainer"]))):
    db = SessionLocal()

    token = str(uuid.uuid4())
    invite = BatchInvite(
        batch_id=batch_id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(days=1)
    )
    db.add(invite)
    db.commit()

    return {"token": token}


@router.post("/join")
def join(token: str, user=Depends(require_role(["student"]))):
    db = SessionLocal()

    invite = db.query(BatchInvite).filter_by(token=token).first()
    if not invite or invite.used:
        raise HTTPException(404, "Invalid invite")

    if invite.expires_at < datetime.utcnow():
        raise HTTPException(400, "Expired")

    db.add(BatchStudent(batch_id=invite.batch_id, student_id=user["user_id"]))
    invite.used = True
    db.commit()

    return {"message": "Joined"}