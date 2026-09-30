from pathlib import Path

from app.services.resume_parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from app.services.text_cleaner import clean_text

from app.services.information_extractor import (
    extract_candidate_profile
)


def process_resume(file_path: str, file_type: str):

    path = Path(file_path)

    if file_type == "application/pdf":
        text = extract_text_from_pdf(str(path))

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(str(path))

    else:
        raise ValueError("Unsupported file type")

    # Clean extracted text
    cleaned_text = clean_text(text)

    # Extract candidate information
    candidate_profile = extract_candidate_profile(cleaned_text)

    # Return both
    return candidate_profile, cleaned_text