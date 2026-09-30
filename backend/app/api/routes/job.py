from fastapi import APIRouter

from app.models.job import JobProfile


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/", response_model=JobProfile)
async def create_job(job: JobProfile):

    return job