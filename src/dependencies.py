from fastapi import Depends, HTTPException, Header
from jose import jwt
from .auth import SECRET_KEY

def get_current_user(token: str = Header(...)):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(401, "Invalid token")

def require_role(roles):
    def wrapper(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(403, "Forbidden")
        return user
    return wrapper