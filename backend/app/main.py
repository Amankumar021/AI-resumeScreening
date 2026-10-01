import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

for candidate in (
    os.environ.get("TESSERACT_CMD"),
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
):
    if candidate and os.path.exists(candidate):
        os.environ["TESSERACT_CMD"] = candidate
        break

from fastapi import FastAPI, Response
from sqlalchemy import inspect, text

from app.database import engine, Base
from app import db_models

from app.api.routes.resume import router as resume_router
from app.api.routes.job import router as job_router
from app.api.routes.screening import router as screening_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.auth import router as auth_router


Base.metadata.create_all(bind=engine)

job_columns = {
    column["name"] for column in inspect(engine).get_columns("jobs")
}
if "seats_available" not in job_columns:
    with engine.begin() as connection:
        connection.execute(text(
            "ALTER TABLE jobs ADD COLUMN seats_available INTEGER NOT NULL DEFAULT 1"
        ))


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


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(
        content=(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">'
            '<rect width="48" height="48" rx="10" fill="#263238"/>'
            '<path d="M14 12h20v6H20v5h12v6H20v7h-6z" fill="#fff"/>'
            '</svg>'
        ),
        media_type="image/svg+xml"
    )