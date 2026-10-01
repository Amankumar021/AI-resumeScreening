MAX_FILE_SIZE = 5 * 1024 * 1024
from pathlib import Path
from uuid import uuid4

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
from app.db_models import CandidateDB, InterviewShortlistDB, ScreeningResultDB
from app.auth import get_current_user
from app.utils.database_utils import list_to_json, json_to_list

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


FILE_TYPES = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    # 1. Validate file type
    extension = Path(file.filename or "").suffix.lower()
    file_type = FILE_TYPES.get(extension)

    if file_type is None:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    # 2. Save uploaded file
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
        status_code=400,
        detail="File size must be less than 5 MB."
    )

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="The uploaded resume is empty."
        )

    file_path = UPLOAD_DIR / f"{uuid4().hex}{extension}"

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # 3. Process resume
    try:
        candidate_profile, resume_text = process_resume(
            str(file_path),
            file_type
        )

    except Exception as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=503 if isinstance(e, RuntimeError) else 422,
            detail=f"Failed to process resume: {str(e)}"
        ) from e

    if not resume_text.strip():
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=422,
            detail="No readable text was found in this resume. For scanned PDFs, install Tesseract OCR."
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

        "content_type": file_type,

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

@router.get("/")
def get_candidates(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    candidates = db.query(CandidateDB).all()

    return [
        {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "skills": json_to_list(candidate.skills),
            "education": json_to_list(candidate.education),
            "experience": json_to_list(candidate.experience),
            "projects": json_to_list(candidate.projects)
        }
        for candidate in candidates
    ]


@router.delete("/")
def clear_candidate_dataset(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    shortlist_count = db.query(InterviewShortlistDB).delete(
        synchronize_session=False
    )
    screening_count = db.query(ScreeningResultDB).delete(
        synchronize_session=False
    )
    candidate_count = db.query(CandidateDB).delete(
        synchronize_session=False
    )
    db.commit()

    deleted_resume_files = 0
    for path in UPLOAD_DIR.iterdir():
        if path.is_file() and path.suffix.lower() in FILE_TYPES:
            path.unlink(missing_ok=True)
            deleted_resume_files += 1

    return {
        "deleted_candidates": candidate_count,
        "deleted_screenings": screening_count,
        "deleted_shortlists": shortlist_count,
        "deleted_resume_files": deleted_resume_files,
        "jobs_preserved": True
    }