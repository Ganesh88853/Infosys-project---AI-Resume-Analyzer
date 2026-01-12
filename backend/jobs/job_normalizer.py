import re
from datetime import datetime, timedelta

def normalize_posted_date(text):
    if not text:
        return None

    text = text.lower()

    if "just now" in text or "today" in text:
        return datetime.now().date()

    match = re.search(r"(\d+)\s+day", text)
    if match:
        return (datetime.now() - timedelta(days=int(match.group(1)))).date()

    match = re.search(r"(\d+)\s+week", text)
    if match:
        return (datetime.now() - timedelta(weeks=int(match.group(1)))).date()

    return None


def detect_job_type(description):
    desc = description.lower()
    if "intern" in desc:
        return "Internship"
    if "contract" in desc:
        return "Contract"
    if "part-time" in desc:
        return "Part-time"
    return "Full-time"


def detect_experience_level(description):
    desc = description.lower()
    if "senior" in desc or "lead" in desc:
        return "Senior"
    if "mid" in desc or "3+" in desc:
        return "Mid"
    return "Entry"


def detect_remote(location, description):
    text = f"{location} {description}".lower()
    return "remote" in text
