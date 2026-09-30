from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.job import JobProfile
from app.database import get_db
from app.db_models import JobDB
from app.utils.database_utils import list_to_json


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

from pydantic import BaseModel
from typing import List, Optional


class JobProfile(BaseModel):
    job_title: Optional[str] = None

    job_description: Optional[str] = None

    required_skills: List[str] = []
    preferred_skills: List[str] = []

    education: List[str] = []

    experience: Optional[str] = None


@router.post("/")
async def create_job(
    job: JobProfile,
    db: Session = Depends(get_db)
):
    db_job = JobDB(
        job_title=job.job_title,
        required_skills=list_to_json(job.required_skills),
        preferred_skills=list_to_json(job.preferred_skills),
        education=list_to_json(job.education),
        experience=job.experience,
        job_description=job.job_description
    )

    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return {
        "message": "Job created successfully",
        "job_id": db_job.id,
        "job": job
    }

@router.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    return {
        "message": "Database connection working"
    }