from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.resume_service import process_resume


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
async def upload_resume(file: UploadFile = File(...)):

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    try:
        extracted_text = process_resume(
            str(file_path),
            file.content_type
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process resume: {str(e)}"
        )

    return {
        "message": "Resume uploaded and processed successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "text": extracted_text
    }