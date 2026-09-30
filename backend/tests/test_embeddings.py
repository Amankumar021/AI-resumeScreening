from app.services.embedding_service import calculate_semantic_similarity


resume = """
Built machine learning models using Python and scikit-learn.
Developed predictive analytics projects.
"""

job_description = """
Looking for a candidate experienced in developing
machine learning systems using Python.
"""

unrelated_text = """
Graphic designer experienced with Photoshop,
Illustrator and visual design.
"""


score1 = calculate_semantic_similarity(
    resume,
    job_description
)

score2 = calculate_semantic_similarity(
    resume,
    unrelated_text
)

print("Resume vs Job:", score1)
print("Resume vs Unrelated:", score2)