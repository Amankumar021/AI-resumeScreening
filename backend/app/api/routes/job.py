from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.job import JobProfile
from app.database import get_db
from app.db_models import JobDB
from app.utils.database_utils import json_to_list, list_to_json
from app.auth import get_current_user

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
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
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

@router.get("/")
def get_jobs(
    db: Session = Depends(get_db)
):
    jobs = db.query(JobDB).all()

    return [
        {
            "id": job.id,
            "job_title": job.job_title,
            "required_skills": json_to_list(
                job.required_skills
            ),
            "preferred_skills": json_to_list(
                job.preferred_skills
            ),
            "education": json_to_list(
                job.education
            ),
            "experience": job.experience,
            "job_description": job.job_description,
        }
        for job in jobs
    ]


@router.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    return {
        "message": "Database connection working"
    }

