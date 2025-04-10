from fastapi import APIRouter, HTTPException
from models.user import UserRegister, UserLogin
from db.mongo import db
from utils.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/register")
def register_user(user: UserRegister):
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")
    user_data = user.dict()
    user_data["password"] = get_password_hash(user_data.pop("password"))
    db.users.insert_one(user_data)
    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(user: UserLogin):
    user_data = db.users.find_one({"email": user.email})
    if not user_data or not verify_password(user.password, user_data['password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.email, "role": user_data['role']}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}