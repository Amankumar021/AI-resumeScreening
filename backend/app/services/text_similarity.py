from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_text_similarity(
    resume_text: str,
    job_description: str
):

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]

    return round(float(similarity), 4)