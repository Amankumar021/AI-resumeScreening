from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.routes.resume import clear_candidate_dataset
from app.database import Base
from app.db_models import (
    CandidateDB,
    InterviewShortlistDB,
    JobDB,
    ScreeningResultDB
)


def test_clear_candidate_dataset_removes_candidate_data_and_resumes(
    monkeypatch,
    tmp_path
):
    engine = create_engine("sqlite://")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    monkeypatch.setattr("app.api.routes.resume.UPLOAD_DIR", tmp_path)
    (tmp_path / "resume.pdf").write_bytes(b"resume")
    (tmp_path / "resume.docx").write_bytes(b"resume")
    (tmp_path / "keep.txt").write_text("unrelated file")

    candidate = CandidateDB(name="Candidate")
    job = JobDB(job_title="Engineer", seats_available=2)
    session.add_all([candidate, job])
    session.commit()
    session.add_all([
        ScreeningResultDB(candidate_id=candidate.id, job_id=job.id, overall_score=90),
        InterviewShortlistDB(candidate_id=candidate.id, job_id=job.id)
    ])
    session.commit()

    result = clear_candidate_dataset(session, "recruiter")

    assert result == {
        "deleted_candidates": 1,
        "deleted_screenings": 1,
        "deleted_shortlists": 1,
        "deleted_resume_files": 2,
        "jobs_preserved": True
    }
    assert session.query(CandidateDB).count() == 0
    assert session.query(ScreeningResultDB).count() == 0
    assert session.query(InterviewShortlistDB).count() == 0
    assert session.query(JobDB).count() == 1
    assert (tmp_path / "keep.txt").exists()

    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()