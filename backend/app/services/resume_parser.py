from pathlib import Path

import fitz
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if path.stat().st_size == 0:
        raise ValueError(f"PDF file is empty: {file_path}")

    try:
        with fitz.open(file_path) as document:
            return "".join(page.get_text() for page in document)
    except (fitz.EmptyFileError, ValueError):
        raise ValueError(f"PDF file is empty or invalid: {file_path}")


def extract_text_from_docx(file_path: str) -> str:
    document = Document(file_path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text)