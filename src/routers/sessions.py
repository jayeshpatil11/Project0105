from fastapi import APIRouter, Depends
from ..dependencies import require_role
from ..database import SessionLocal
from ..models import Session

router = APIRouter()

@router.post("/")
def create_session(batch_id: int, title: str,
                   user=Depends(require_role(["trainer"]))):
    db = SessionLocal()

    s = Session(batch_id=batch_id, trainer_id=user["user_id"], title=title)
    db.add(s)
    db.commit()

    return {"session_id": s.id}