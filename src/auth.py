from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Fix bcrypt 72 byte issue
    if not isinstance(password, str):
        password = str(password)
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_token(data: dict, expires=24):
    data.update({"exp": datetime.utcnow() + timedelta(hours=expires)})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)