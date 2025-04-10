from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from utils.auth import SECRET_KEY, ALGORITHM

def get_current_user(token: str = Header(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(role: str):
    def wrapper(user: dict = Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return user
    return wrapper