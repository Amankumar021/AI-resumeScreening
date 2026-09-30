import re

from app.models.candidate import CandidateProfile


SKILL_LIST = [
    "Python",
    "C++",
    "Java",
    "JavaScript",
    "TypeScript",
    "React",
    "Node.js",
    "SQL",
    "MongoDB",
    "PostgreSQL",
    "Git",
    "Docker",
    "AWS",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "FastAPI",
    "Django",
    "Pandas",
    "NumPy",
    "scikit-learn"
]


SECTION_HEADERS = {
    "education",
    "skills",
    "experience",
    "work experience",
    "projects",
    "certifications",
    "summary",
    "objective"
}


def extract_email(text: str):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_phone(text: str):
    pattern = r"(?:\+91[-\s]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_name(text: str):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    ignored_headers = {
        "resume",
        "curriculum vitae",
        "cv"
    }

    for line in lines[:5]:
        if line.lower() not in ignored_headers:
            return line

    return None


def extract_skills(text: str):

    text_lower = text.lower()

    found_skills = []

    for skill in SKILL_LIST:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills


def extract_sections(text: str):

    sections = {}

    current_section = None

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        normalized = line.lower()

        if normalized in SECTION_HEADERS:

            current_section = normalized
            sections[current_section] = []

        elif current_section:
            sections[current_section].append(line)

    return sections


def extract_candidate_profile(text: str):

    sections = extract_sections(text)

    education = sections.get("education", [])

    experience = sections.get(
        "experience",
        sections.get("work experience", [])
    )

    projects = sections.get("projects", [])

    candidate = CandidateProfile(
        name=extract_name(text),
        email=extract_email(text),
        phone=extract_phone(text),
        skills=extract_skills(text),
        education=education,
        experience=experience,
        projects=projects
    )

    return candidate