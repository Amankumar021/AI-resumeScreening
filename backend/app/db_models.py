from sqlalchemy import Column, Integer, String, Text, Float, UniqueConstraint
from app.database import Base
from sqlalchemy import Boolean

class CandidateDB(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    skills = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    projects = Column(Text, nullable=True)

    resume_text = Column(Text, nullable=True)


class JobDB(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    job_title = Column(String, nullable=True)
    seats_available = Column(Integer, nullable=False, default=1)

    required_skills = Column(Text, nullable=True)
    preferred_skills = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    experience = Column(String, nullable=True)

    job_description = Column(Text, nullable=True)


class ScreeningResultDB(Base):
    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(Integer, nullable=False)
    job_id = Column(Integer, nullable=False)

    required_skill_score = Column(Float)
    preferred_skill_score = Column(Float)
    tfidf_score = Column(Float)
    semantic_score = Column(Float)
    overall_score = Column(Float)


class InterviewShortlistDB(Base):
    __tablename__ = "interview_shortlists"
    __table_args__ = (
        UniqueConstraint("candidate_id", "job_id", name="uq_shortlist_candidate_job"),
    )

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, nullable=False, index=True)
    job_id = Column(Integer, nullable=False, index=True)


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )