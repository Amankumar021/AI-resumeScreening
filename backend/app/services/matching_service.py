def calculate_skill_match(
    candidate_skills,
    required_skills
):
    candidate_set = {
        skill.lower()
        for skill in candidate_skills
    }

    required_set = {
        skill.lower()
        for skill in required_skills
    }

    matched_skills = candidate_set & required_set
    missing_skills = required_set - candidate_set

    if not required_set:
        match_percentage = 0.0
    else:
        match_percentage = (
            len(matched_skills)
            / len(required_set)
        ) * 100

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "match_percentage": round(match_percentage, 2)
    }