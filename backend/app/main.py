from fastapi import FastAPI

from app.api.routes.resume import router as resume_router


app = FastAPI(
    title="AI Resume Screening System",
    description="AI-powered resume screening and candidate analysis API",
    version="1.0.0"
)


app.include_router(resume_router)


@app.get("/")
def home():
    return {
        "message": "AI Resume Screening API is running",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {
        "message": "AI Resume Screening API is running"
    }