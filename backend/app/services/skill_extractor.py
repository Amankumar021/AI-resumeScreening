import re

from app.utils.skills import SKILL_LIST


def extract_skills(text: str):
    text_lower = text.lower()
    found_skills = []

    for skill in SKILL_LIST:
        pattern = r"(?<![a-z0-9+/#])" + re.escape(skill.lower()) + r"(?![a-z0-9+/#])"
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills