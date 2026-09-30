from app.services.text_similarity import calculate_text_similarity


resume = """
Python developer with experience in SQL.
Built machine learning projects using Python.
"""


job = """
Looking for a graphic designer with experience
in Photoshop, Illustrator and visual branding.
"""


score = calculate_text_similarity(
    resume,
    job
)


print("Similarity:", score)