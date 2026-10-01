from app.services.matching_service import (
    calculate_ats_score,
    calculate_preferred_skill_match,
    calculate_skill_match,
)


def test_required_skills_match_case_and_punctuation_variants():
    result = calculate_skill_match(
        ["NODE JS", "Postgres", "C++"],
        ["Node.js", "PostgreSQL", "C#"]
    )

    assert result == {
        "matched_skills": ["node.js", "postgresql"],
        "missing_skills": ["c#"],
        "match_percentage": 66.67
    }


def test_preferred_skills_match_independently_from_required_skills():
    candidate_skills = ["python", "React.js"]

    required = calculate_skill_match(candidate_skills, ["Python", "SQL"])
    preferred = calculate_preferred_skill_match(
        candidate_skills,
        ["React", "AWS"]
    )

    assert required["matched_skills"] == ["python"]
    assert required["missing_skills"] == ["sql"]
    assert preferred["matched_skills"] == ["react"]
    assert preferred["match_percentage"] == 50.0


def test_ats_score_weights_required_skills_more_than_preferred_skills():
    ats_score = calculate_ats_score(
        ["python", "sql", "react"],
        ["python", "sql", "docker"],
        ["react", "aws"]
    )

    assert ats_score == 70.0