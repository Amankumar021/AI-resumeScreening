import fitz

from app.services import resume_parser


def test_pdf_parser_uses_native_text_when_available(tmp_path):
    pdf_path = tmp_path / "text-resume.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Native resume text")
    document.save(pdf_path)
    document.close()

    assert resume_parser.extract_text_from_pdf(str(pdf_path)) == "Native resume text"


def test_pdf_parser_uses_ocr_for_image_only_pages(monkeypatch, tmp_path):
    pdf_path = tmp_path / "scanned-resume.pdf"
    document = fitz.open()
    document.new_page()
    document.save(pdf_path)
    document.close()

    monkeypatch.setattr(resume_parser, "_ocr_page", lambda page: "OCR resume text")

    assert resume_parser.extract_text_from_pdf(str(pdf_path)) == "OCR resume text"


def test_ocr_uses_tesseract_command_from_environment(monkeypatch):
    import pytesseract

    configured_command = r"C:\OCR\tesseract.exe"
    monkeypatch.setenv("TESSERACT_CMD", configured_command)
    monkeypatch.setattr(pytesseract, "image_to_string", lambda image: "OCR text")

    document = fitz.open()
    try:
        assert resume_parser._ocr_page(document.new_page()) == "OCR text"
    finally:
        document.close()

    assert pytesseract.pytesseract.tesseract_cmd == configured_command