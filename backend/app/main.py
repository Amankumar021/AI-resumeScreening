from fastapi import FastAPI

from app.api.routes.resume import router as resume_router
from app.api.routes.job import router as job_router


app = FastAPI(
    title="AI Resume Screening System",
    description="AI-powered resume screening and candidate analysis API",
    version="1.0.0"
)


app.include_router(resume_router)
app.include_router(job_router)


@app.get("/")
def root():
    return {
        "message": "AI Resume Screening API is running"
    }