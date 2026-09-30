from app.services.matching_service import calculate_skill_match


candidate_skills = [
    "Python",
    "C++",
    "SQL",
    "React"
]

required_skills = [
    "Python",
    "C++",
    "SQL",
    "Git"
]


result = calculate_skill_match(
    candidate_skills,
    required_skills
)


print(result)


def calculate_preferred_skill_match(
    candidate_skills,
    preferred_skills
):
    candidate_set = {
        skill.lower()
        for skill in candidate_skills
    }

    preferred_set = {
        skill.lower()
        for skill in preferred_skills
    }

    matched_skills = candidate_set & preferred_set
    missing_skills = preferred_set - candidate_set

    if not preferred_set:
        match_percentage = 0.0
    else:
        match_percentage = (
            len(matched_skills)
            / len(preferred_set)
        ) * 100

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "match_percentage": round(match_percentage, 2)
    }

def analyze_candidate(candidate_skills, job):
    required_result = calculate_skill_match(
        candidate_skills,
        job.required_skills
    )

    preferred_result = calculate_preferred_skill_match(
        candidate_skills,
        job.preferred_skills
    )

    return {
        "required_skills": required_result,
        "preferred_skills": preferred_result
    }