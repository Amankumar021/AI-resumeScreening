import io
import os
import shutil
from pathlib import Path

try:
    import fitz
except ModuleNotFoundError as exc:
    fitz = None
    FITZ_IMPORT_ERROR = exc
else:
    FITZ_IMPORT_ERROR = None


def _get_tesseract_cmd() -> str:
    configured = os.environ.get("TESSERACT_CMD")
    if configured and configured.strip():
        return configured.strip()

    which_tesseract = shutil.which("tesseract")
    if which_tesseract:
        return which_tesseract

    for candidate in (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ):
        if os.path.exists(candidate):
            return candidate

    return "tesseract"


def _require_fitz():
    if fitz is None:
        raise RuntimeError(
            "PyMuPDF (fitz) is not installed. Run: pip install -r requirements.txt"
        ) from FITZ_IMPORT_ERROR


def _ocr_page(page) -> str:
    try:
        import pytesseract
        from PIL import Image
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "OCR dependencies are missing. Install pytesseract and Pillow, "
            "and install the Tesseract OCR executable."
        ) from exc

    pytesseract.pytesseract.tesseract_cmd = _get_tesseract_cmd()

    pixmap = page.get_pixmap(
        matrix=fitz.Matrix(2.5, 2.5),
        alpha=False
    )
    image_bytes = pixmap.tobytes("png")

    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            return pytesseract.image_to_string(image)
    except pytesseract.pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR executable was not found. Install Tesseract OCR, "
            "add it to PATH, or set TESSERACT_CMD to its full executable path."
        ) from exc


def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if path.stat().st_size == 0:
        raise ValueError(f"PDF file is empty: {file_path}")

    _require_fitz()

    try:
        with fitz.open(file_path) as document:
            page_text = []
            for page in document:
                text = page.get_text().strip()
                if not text:
                    text = _ocr_page(page).strip()
                page_text.append(text)

            return "\n".join(text for text in page_text if text)
    except (fitz.EmptyFileError, ValueError):
        raise ValueError(f"PDF file is empty or invalid: {file_path}")


def extract_text_from_docx(file_path: str) -> str:
    try:
        from docx import Document
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "python-docx is not installed. Run: pip install python-docx"
        ) from exc

    document = Document(file_path)
    return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text)