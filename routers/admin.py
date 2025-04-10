from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import pandas as pd
from db.mongo import db
from utils.deps import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/upload-students")
def upload_students(file: UploadFile = File(...), user=Depends(require_role("admin"))):
    df = pd.read_csv(file.file)
    allowed_emails = df["email"].dropna().str.lower().tolist()
    records = [{"email": email, "name": df[df['email'] == email]['name'].values[0]} for email in allowed_emails]
    db.allowed_students.delete_many({})
    db.allowed_students.insert_many(records)
    return {"message": "Students uploaded", "total": len(records)}

@router.get("/users")
def get_all_users(user=Depends(require_role("admin"))):
    users = list(db.users.find({}, {"_id": 0, "email": 1, "name": 1, "role": 1}))
    return users