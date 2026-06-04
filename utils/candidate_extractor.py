import re


def extract_email(text):

    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

    match = re.search(
        pattern,
        text
    )

    return match.group(0) if match else ""


def extract_phone(text):

    match = re.search(
        r'(\+91[\-\s]?)?[6-9]\d{9}',
        text
    )

    if match:

        return match.group()

    return ""


def extract_name(text):

    ignore_words = [
        "curriculum vitae",
        "resume",
        "cv",
        "profile",
        "professional summary"
    ]

    lines = text.split("\n")

    for line in lines[:20]:

        line = line.strip()

        if not line:
            continue

        if line.lower() in ignore_words:
            continue

        if "@" in line:
            continue

        if re.search(r"\d", line):
            continue

        words = line.split()

        if 2 <= len(words) <= 4:

            return line.title()

    return "Unknown"