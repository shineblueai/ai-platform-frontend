from fastapi import FastAPI
from routers import user, resume, exam

app = FastAPI(title="AI Hiring Platform")

app.include_router(user.router)
app.include_router(resume.router)
app.include_router(exam.router)
app.include_router(admin.router)

from routers import user, resume, exam, admin



@app.get("/")
def root():
    return {"message": "Welcome to AI Hiring Platform 🚀"}