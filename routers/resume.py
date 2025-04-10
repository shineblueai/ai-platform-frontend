from fastapi import APIRouter, UploadFile, Form, Depends
import tempfile
from db.mongo import db
from datetime import datetime
from services.resume_analysis import extract_text_from_pdf, analyze_resume_with_jd
from services.pdf_generator import create_resume_match_pdf
from fastapi.responses import FileResponse
from utils.deps import get_current_user

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/analyze")
async def resume_jd_match(resume: UploadFile, job_description: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await resume.read())
        tmp_path = tmp.name

    resume_text = extract_text_from_pdf(tmp_path)
    result = analyze_resume_with_jd(resume_text, job_description)

    return {"analysis": result}

@router.post("/analyze/save")
async def resume_jd_match_and_save(resume: UploadFile, job_description: str = Form(...), user=Depends(get_current_user)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await resume.read())
        tmp_path = tmp.name

    resume_text = extract_text_from_pdf(tmp_path)
    result = analyze_resume_with_jd(resume_text, job_description)

    record = {
        "email": user["sub"],
        "role": user["role"],
        "job_description": job_description,
        "resume_text": resume_text,
        "analysis": result,
        "timestamp": datetime.now()
    }
    db.resumes.insert_one(record)
    return {"analysis": result, "message": "Saved successfully"}

@router.post("/analyze/pdf")
async def resume_jd_pdf(resume: UploadFile, job_description: str = Form(...), user=Depends(get_current_user)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await resume.read())
        tmp_path = tmp.name

    resume_text = extract_text_from_pdf(tmp_path)
    result = analyze_resume_with_jd(resume_text, job_description)

    pdf_path = create_resume_match_pdf(user["sub"], job_description, result)
    return FileResponse(pdf_path, filename=os.path.basename(pdf_path), media_type='application/pdf')