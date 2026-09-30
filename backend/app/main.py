import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

from fastapi import FastAPI

from app.database import engine, Base
from app import db_models

from app.api.routes.resume import router as resume_router
from app.api.routes.job import router as job_router
from app.api.routes.screening import router as screening_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.auth import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Resume Screening System",
    description="AI-powered resume screening and candidate analysis API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(resume_router)
app.include_router(job_router)
app.include_router(screening_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "AI Resume Screening API is running"
    }