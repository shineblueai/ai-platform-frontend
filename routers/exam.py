from fastapi import APIRouter, Depends
from db.mongo import db
from utils.deps import require_role
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/exam", tags=["Exam"])

class ExamCreate(BaseModel):
    title: str
    description: str
    tech_stack: str
    questions: list

@router.post("/create")
def create_exam(exam: ExamCreate, user=Depends(require_role("company"))):
    exam_data = exam.dict()
    exam_data["created_by"] = user["sub"]
    exam_data["created_at"] = datetime.now()
    db.exams.insert_one(exam_data)
    return {"message": "Exam created successfully"}