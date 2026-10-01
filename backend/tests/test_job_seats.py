import asyncio

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.routes.job import JobProfile, create_job, get_jobs
from app.database import Base
from app.db_models import JobDB


def test_create_job_persists_available_seats():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()

    asyncio.run(create_job(
        JobProfile(job_title="Engineer", seats_available=4),
        session,
        "recruiter"
    ))

    jobs = get_jobs(session, "recruiter")
    assert jobs[0]["seats_available"] == 4
    assert session.query(JobDB).count() == 1

    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_job_seats_must_be_positive():
    with pytest.raises(ValidationError):
        JobProfile(job_title="Engineer", seats_available=0)