import re


def clean_text(text: str) -> str:

    # Replace multiple spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text