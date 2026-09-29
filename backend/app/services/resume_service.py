from pathlib import Path

from app.services.resume_parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from app.services.text_cleaner import clean_text


def process_resume(file_path: str, file_type: str) -> str:

    path = Path(file_path)

    if file_type == "application/pdf":
        text = extract_text_from_pdf(str(path))

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(str(path))

    else:
        raise ValueError("Unsupported file type")

    cleaned_text = clean_text(text)

    return cleaned_text