from app.models.job import JobProfile
from app.services.skill_extractor import extract_skills


SECTION_ALIASES = {
    "required skills": "required_skills",
    "required skill": "required_skills",
    "must have": "required_skills",

    "preferred skills": "preferred_skills",
    "preferred skill": "preferred_skills",
    "nice to have": "preferred_skills",

    "education": "education",
    "qualification": "education",

    "experience": "experience",
    "work experience": "experience"
}


def extract_job_title(text: str):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    ignored_headers = {
        "job description",
        "job posting",
        "jd"
    }

    for line in lines[:5]:

        if line.lower() not in ignored_headers:
            return line

    return None


def parse_job_description(text: str):

    sections = {}
    current_section = None

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        normalized = line.lower().rstrip(":")

        if normalized in SECTION_ALIASES:

            current_section = SECTION_ALIASES[normalized]

            sections[current_section] = []

        elif current_section:

            sections[current_section].append(line)

    required_text = " ".join(
        sections.get("required_skills", [])
    )

    preferred_text = " ".join(
        sections.get("preferred_skills", [])
    )

    education = sections.get("education", [])

    experience_list = sections.get("experience", [])

    experience = (
        " ".join(experience_list)
        if experience_list
        else None
    )

    return JobProfile(
        job_title=extract_job_title(text),
        required_skills=extract_skills(required_text),
        preferred_skills=extract_skills(preferred_text),
        education=education,
        experience=experience
    )