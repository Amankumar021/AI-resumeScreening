import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.routes.screening import (
    get_interview_shortlist,
    remove_candidate_from_interview_shortlist,
    shortlist_candidate_for_interview
)
from app.database import Base
from app.db_models import (
    CandidateDB,
    InterviewShortlistDB,
    JobDB,
    ScreeningResultDB
)


@pytest.fixture
def db_session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_shortlist_is_saved_per_job_and_can_be_removed(db_session):
    candidate = CandidateDB(name="Avery Candidate", email="avery@example.com")
    job = JobDB(job_title="Data Analyst")
    db_session.add_all([candidate, job])
    db_session.commit()

    screening = ScreeningResultDB(
        candidate_id=candidate.id,
        job_id=job.id,
        overall_score=92.5
    )
    db_session.add(screening)
    db_session.commit()

    first_save = shortlist_candidate_for_interview(
        candidate.id,
        job.id,
        db_session,
        "recruiter"
    )
    repeated_save = shortlist_candidate_for_interview(
        candidate.id,
        job.id,
        db_session,
        "recruiter"
    )
    entries = get_interview_shortlist(db_session, "recruiter")

    assert first_save["shortlisted"] is True
    assert repeated_save["id"] == first_save["id"]
    assert len(entries) == 1
    assert entries[0]["candidate"]["name"] == "Avery Candidate"
    assert entries[0]["job"]["title"] == "Data Analyst"
    assert entries[0]["overall_score"] == 92.5

    removed = remove_candidate_from_interview_shortlist(
        candidate.id,
        job.id,
        db_session,
        "recruiter"
    )

    assert removed["shortlisted"] is False
    assert db_session.query(InterviewShortlistDB).count() == 0


def test_candidate_must_be_screened_for_job_before_shortlisting(db_session):
    candidate = CandidateDB(name="Avery Candidate")
    job = JobDB(job_title="Data Analyst")
    db_session.add_all([candidate, job])
    db_session.commit()

    with pytest.raises(HTTPException) as error:
        shortlist_candidate_for_interview(
            candidate.id,
            job.id,
            db_session,
            "recruiter"
        )

    assert error.value.status_code == 404