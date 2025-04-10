from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str  # student / company / admin

class UserLogin(BaseModel):
    email: EmailStr
    password: str