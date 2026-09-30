DEFAULT_WEIGHTS = {
    "required_skills": 0.40,
    "preferred_skills": 0.10,
    "tfidf": 0.15,
    "semantic": 0.35
}


def calculate_final_score(
    required_skill_percentage,
    preferred_skill_percentage,
    tfidf_similarity,
    semantic_similarity,
    weights=DEFAULT_WEIGHTS
):
    tfidf_percentage = tfidf_similarity * 100
    semantic_percentage = semantic_similarity * 100

    score = (
        required_skill_percentage
        * weights["required_skills"]
        +
        preferred_skill_percentage
        * weights["preferred_skills"]
        +
        tfidf_percentage
        * weights["tfidf"]
        +
        semantic_percentage
        * weights["semantic"]
    )

    return round(score, 2)