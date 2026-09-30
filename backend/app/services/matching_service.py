from app.services.text_similarity import calculate_text_similarity
from app.services.embedding_service import calculate_semantic_similarity
from app.services.scoring_service import calculate_final_score

def calculate_skill_match(candidate_skills, required_skills):
    candidate_set = {skill.lower() for skill in candidate_skills}
    required_set = {skill.lower() for skill in required_skills}

    matched_skills = candidate_set & required_set
    missing_skills = required_set - candidate_set

    if not required_set:
        match_percentage = 0.0
    else:
        match_percentage = (
            len(matched_skills) / len(required_set)
        ) * 100

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "match_percentage": round(match_percentage, 2)
    }


def calculate_preferred_skill_match(
    candidate_skills,
    preferred_skills
):
    candidate_set = {skill.lower() for skill in candidate_skills}
    preferred_set = {skill.lower() for skill in preferred_skills}

    matched_skills = candidate_set & preferred_set

    if not preferred_set:
        match_percentage = 0.0
    else:
        match_percentage = (
            len(matched_skills) / len(preferred_set)
        ) * 100

    return {
        "matched_skills": sorted(matched_skills),
        "match_percentage": round(match_percentage, 2)
    }


def calculate_semantic_match(resume_text, job_description):
    return calculate_semantic_similarity(
        resume_text,
        job_description
    )


def analyze_candidate(
    candidate,
    job,
    resume_text,
    job_description
):
    required_match = calculate_skill_match(
        candidate.skills,
        job.required_skills
    )

    preferred_match = calculate_preferred_skill_match(
        candidate.skills,
        job.preferred_skills
    )

    tfidf_score = calculate_text_similarity(
        resume_text,
        job_description
    )

    semantic_score = calculate_semantic_match(
        resume_text,
        job_description
    )

    final_score = calculate_final_score(
        required_match["match_percentage"],
        preferred_match["match_percentage"],
        tfidf_score,
        semantic_score
    )

    return {
        "candidate": candidate.name,
        "required_skill_match": required_match,
        "preferred_skill_match": preferred_match,
        "tfidf_similarity": tfidf_score,
        "semantic_similarity": semantic_score,
        "overall_relevance_score": final_score
    }