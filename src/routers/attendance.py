from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import require_role
from ..database import SessionLocal
from ..models import Session, Attendance, BatchStudent

router = APIRouter()

@router.post("/mark")
def mark(session_id: int, status: str,
         user=Depends(require_role(["student"]))):

    db = SessionLocal()

    session = db.query(Session).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(404, "Session not found")

    enrolled = db.query(BatchStudent).filter_by(
        batch_id=session.batch_id,
        student_id=user["user_id"]
    ).first()

    if not enrolled:
        raise HTTPException(403, "Not enrolled")

    db.add(Attendance(
        session_id=session_id,
        student_id=user["user_id"],
        status=status
    ))
    db.commit()

    return {"message": "Marked"}