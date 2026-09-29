from pathlib import Path

# from fastapi import APIRouter, UploadFile, File

from fastapi import APIRouter, UploadFile, File,HTTPException


router = APIRouter(
    prefix="/api/v1/resumes",
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
            detail="Only pdf and DOCX files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    return {
        "message" : "Resume uploaded successfully", 
        "filename": file.filename,
        "content_type": file.content_type,
        "path": str(file_path)
    }