from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.db_models import (
    CandidateDB,
    JobDB,
    ScreeningResultDB,
    InterviewShortlistDB
)

from app.utils.database_utils import json_to_list

from app.services.matching_service import (
    calculate_skill_match,
    calculate_preferred_skill_match
)

from app.services.text_similarity import calculate_text_similarity
from app.services.embedding_service import calculate_semantic_similarity
from app.services.scoring_service import calculate_final_score

from app.auth import get_current_user

router = APIRouter(
    prefix="/screening",
    tags=["Screening"]
)


@router.post("/{candidate_id}/{job_id}")
def screen_candidate(
    candidate_id: int,
    job_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    # --------------------------------
    # 1. Get candidate
    # --------------------------------

    candidate = db.query(CandidateDB).filter(
        CandidateDB.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    # --------------------------------
    # 2. Get job
    # --------------------------------

    job = db.query(JobDB).filter(
        JobDB.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # --------------------------------
    # 3. Convert database JSON
    #    back to Python lists
    # --------------------------------

    candidate_skills = json_to_list(
        candidate.skills
    )

    required_skills = json_to_list(
        job.required_skills
    )

    preferred_skills = json_to_list(
        job.preferred_skills
    )

    # --------------------------------
    # 4. Required skill matching
    # --------------------------------

    required_match = calculate_skill_match(
        candidate_skills,
        required_skills
    )

    # --------------------------------
    # 5. Preferred skill matching
    # --------------------------------

    preferred_match = calculate_preferred_skill_match(
        candidate_skills,
        preferred_skills
    )

    # --------------------------------
    # 6. TF-IDF similarity
    # --------------------------------

    tfidf_score = calculate_text_similarity(
        candidate.resume_text or "",
        job.job_description or ""
    )

    # --------------------------------
    # 7. Semantic similarity
    # --------------------------------

    semantic_score = calculate_semantic_similarity(
        candidate.resume_text or "",
        job.job_description or ""
    )

    # --------------------------------
    # 8. Overall score
    # --------------------------------

    overall_score = calculate_final_score(
        required_match["match_percentage"],
        preferred_match["match_percentage"],
        tfidf_score,
        semantic_score
    )

    # --------------------------------
    # 9. Save result
    # --------------------------------

    result = ScreeningResultDB(
        candidate_id=candidate_id,
        job_id=job_id,

        required_skill_score=(
            required_match["match_percentage"]
        ),

        preferred_skill_score=(
            preferred_match["match_percentage"]
        ),

        tfidf_score=tfidf_score,

        semantic_score=semantic_score,

        overall_score=overall_score
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    # --------------------------------
    # 10. Return result
    # --------------------------------

    return {
    "screening_id": result.id,

    "candidate": {
        "id": candidate.id,
        "name": candidate.name,
        "email": candidate.email
    },

    "job": {
        "id": job.id,
        "title": job.job_title
    },

    "analysis": {
        "required_skill_match": required_match,
        "preferred_skill_match": preferred_match,
        "tfidf_similarity": tfidf_score,
        "semantic_similarity": semantic_score,
        "overall_relevance_score": overall_score
    }
}

@router.get("/")
def get_screening_results(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):

    results = db.query(ScreeningResultDB).all()

    response = []

    for result in results:

        candidate = db.query(CandidateDB).filter(
            CandidateDB.id == result.candidate_id
        ).first()

        job = db.query(JobDB).filter(
            JobDB.id == result.job_id
        ).first()

        response.append({
            "id": result.id,

            "candidate": {
                "id": candidate.id if candidate else None,
                "name": candidate.name if candidate else "Unknown",
                "email": candidate.email if candidate else None
            },

            "job": {
                "id": job.id if job else None,
                "title": job.job_title if job else "Unknown"
            },

            "required_skill_score":
                result.required_skill_score,

            "preferred_skill_score":
                result.preferred_skill_score,

            "tfidf_score":
                result.tfidf_score,

            "semantic_score":
                result.semantic_score,

            "overall_score":
                result.overall_score
        })

    return response


@router.get("/shortlist/")
def get_interview_shortlist(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    entries = db.query(InterviewShortlistDB).all()
    response = []

    for entry in entries:
        candidate = db.query(CandidateDB).filter(
            CandidateDB.id == entry.candidate_id
        ).first()
        job = db.query(JobDB).filter(
            JobDB.id == entry.job_id
        ).first()
        screening = db.query(ScreeningResultDB).filter(
            ScreeningResultDB.candidate_id == entry.candidate_id,
            ScreeningResultDB.job_id == entry.job_id
        ).order_by(ScreeningResultDB.id.desc()).first()

        response.append({
            "id": entry.id,
            "candidate_id": entry.candidate_id,
            "job_id": entry.job_id,
            "overall_score": screening.overall_score if screening else None,
            "candidate": {
                "id": candidate.id if candidate else None,
                "name": candidate.name if candidate else "Unknown",
                "email": candidate.email if candidate else None
            },
            "job": {
                "id": job.id if job else None,
                "title": job.job_title if job else "Unknown"
            }
        })

    return response


@router.post("/shortlist/{candidate_id}/{job_id}")
def shortlist_candidate_for_interview(
    candidate_id: int,
    job_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    screening = db.query(ScreeningResultDB).filter(
        ScreeningResultDB.candidate_id == candidate_id,
        ScreeningResultDB.job_id == job_id
    ).first()

    if not screening:
        raise HTTPException(
            status_code=404,
            detail="Screen the candidate for this job before shortlisting."
        )

    entry = db.query(InterviewShortlistDB).filter(
        InterviewShortlistDB.candidate_id == candidate_id,
        InterviewShortlistDB.job_id == job_id
    ).first()

    if not entry:
        entry = InterviewShortlistDB(
            candidate_id=candidate_id,
            job_id=job_id
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)

    return {
        "id": entry.id,
        "candidate_id": candidate_id,
        "job_id": job_id,
        "shortlisted": True
    }


@router.delete("/shortlist/{candidate_id}/{job_id}")
def remove_candidate_from_interview_shortlist(
    candidate_id: int,
    job_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    entry = db.query(InterviewShortlistDB).filter(
        InterviewShortlistDB.candidate_id == candidate_id,
        InterviewShortlistDB.job_id == job_id
    ).first()

    if entry:
        db.delete(entry)
        db.commit()

    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "shortlisted": False
    }