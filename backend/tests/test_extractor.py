from app.services.information_extractor import (
    extract_email,
    extract_phone,
    extract_skills,
)


def test_extract_email_and_phone():
    text = """
    AMAN KUMAR

    Email: aman@gmail.com
    Phone: 9876543210

    Skills:
    Python
    C++
    SQL
    """

    assert extract_email(text) == "aman@gmail.com"
    assert extract_phone(text) == "9876543210"
    assert extract_skills(text) == ["Python", "C++", "SQL"]


def test_extract_custom_skills_from_explicit_skill_section():
    text = """
    Technical Skills:
    Kubernetes, stakeholder management
    """

    assert extract_skills(text) == ["Kubernetes", "stakeholder management"]


def test_extract_skills_from_categorized_resume_rows():
    text = """
    Skills
    Programming Languages: C, C++, Java, Python
    Web Development: HTML, CSS, JavaScript, React, Node.js, Express.js, MongoDB
    Problem Solving & DSA: 4 star on HackerRank, 1000+ questions on Codolio
    """

    skills = extract_skills(text)

    assert "C" in skills
    assert "Express.js" in skills
    assert "MongoDB" in skills
    assert "4 star on HackerRank" not in skills
    assert "1000+ questions on Codolio" not in skills


if __name__ == "__main__":
    test_extract_email_and_phone()
    print("extract_email, extract_phone and extract_skills passed")