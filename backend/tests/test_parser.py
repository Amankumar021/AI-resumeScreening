import sys
from pathlib import Path

from app.services.resume_parser import extract_text_from_pdf

BASE_DIR = Path(__file__).resolve().parent.parent
candidates = [
    BASE_DIR / "uploads" / "resume.pdf",
    BASE_DIR / "uploads" / "16511249.pdf",
    BASE_DIR / "uploads" / "23628651.pdf",
]
file_path = next(
    (path for path in candidates if path.exists() and path.stat().st_size > 0),
    candidates[0],
)

text = extract_text_from_pdf(str(file_path))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print(text)