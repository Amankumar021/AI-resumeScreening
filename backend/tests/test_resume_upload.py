import asyncio
from io import BytesIO
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from starlette.datastructures import Headers, UploadFile

from app.api.routes import resume


class FakeSession:
    def add(self, candidate):
        self.candidate = candidate

    def commit(self):
        pass

    def refresh(self, candidate):
        candidate.id = 42


def make_upload(filename, content_type="application/octet-stream"):
    return UploadFile(
        file=BytesIO(b"resume file bytes"),
        filename=filename,
        headers=Headers({"content-type": content_type})
    )


def test_upload_uses_file_extension_when_mime_type_is_generic(monkeypatch, tmp_path):
    monkeypatch.setattr(resume, "UPLOAD_DIR", tmp_path)
    processed = {}

    def fake_process_resume(path, file_type):
        processed["file_type"] = file_type
        return (
            SimpleNamespace(
                name="Candidate",
                email="candidate@example.com",
                phone=None,
                skills=["Python"],
                education=[],
                experience=[],
                projects=[]
            ),
            "Candidate resume text"
        )

    monkeypatch.setattr(resume, "process_resume", fake_process_resume)

    result = asyncio.run(
        resume.upload_resume(
            make_upload("candidate.PDF"),
            FakeSession(),
            "recruiter"
        )
    )

    assert processed["file_type"] == "application/pdf"
    assert result["candidate_id"] == 42
    assert len(list(tmp_path.iterdir())) == 1


def test_upload_reports_ocr_error_and_removes_temporary_file(
    monkeypatch,
    tmp_path
):
    monkeypatch.setattr(resume, "UPLOAD_DIR", tmp_path)

    def fail_to_process(path, file_type):
        raise RuntimeError("Tesseract OCR executable was not found")

    monkeypatch.setattr(resume, "process_resume", fail_to_process)

    with pytest.raises(HTTPException) as error:
        asyncio.run(
            resume.upload_resume(
                make_upload("scanned.pdf", "application/pdf"),
                FakeSession(),
                "recruiter"
            )
        )

    assert error.value.status_code == 503
    assert "Tesseract OCR executable was not found" in error.value.detail
    assert list(tmp_path.iterdir()) == []