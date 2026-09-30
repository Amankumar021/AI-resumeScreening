from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

from app.services.resume_service import process_resume

from app.database import get_db
from app.db_models import CandidateDB

from app.utils.database_utils import list_to_json


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 1. Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    # 2. Save uploaded file
    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # 3. Process resume
    try:
        candidate_profile, resume_text = process_resume(
            str(file_path),
            file.content_type
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process resume: {str(e)}"
        )

    # 4. Create database candidate
    db_candidate = CandidateDB(
        name=candidate_profile.name,
        email=candidate_profile.email,
        phone=candidate_profile.phone,

        skills=list_to_json(
            candidate_profile.skills
        ),

        education=list_to_json(
            candidate_profile.education
        ),

        experience=list_to_json(
            candidate_profile.experience
        ),

        projects=list_to_json(
            candidate_profile.projects
        ),

        resume_text=resume_text
    )

    # 5. Save candidate to database
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    # 6. Return response
    return {
        "message": "Resume uploaded and processed successfully",

        "candidate_id": db_candidate.id,

        "filename": file.filename,

        "content_type": file.content_type,

        "candidate": {
            "name": candidate_profile.name,
            "email": candidate_profile.email,
            "phone": candidate_profile.phone,
            "skills": candidate_profile.skills,
            "education": candidate_profile.education,
            "experience": candidate_profile.experience,
            "projects": candidate_profile.projects
        }
    }