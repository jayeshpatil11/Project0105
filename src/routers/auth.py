from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from ..database import SessionLocal
from ..models import User
from ..auth import hash_password, verify_password, create_token
from ..schemas import SignupRequest, LoginRequest

router = APIRouter()

@router.post("/signup")
def signup(data: SignupRequest):
    db = SessionLocal()

    try:
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password),
            role=data.role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "User created",
            "token": create_token({"user_id": user.id, "role": data.role})
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()


@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "token": create_token({"user_id": user.id, "role": user.role})
    }