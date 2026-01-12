def calculate_skill_match(user_skills, required_skills):
    if not required_skills:
        return 100

    matched = set(user_skills) & set(required_skills)
    return (len(matched) / len(required_skills)) * 100


def experience_match(user_level, required_level):
    levels = ["junior", "mid", "senior", "lead"]

    if required_level not in levels or user_level not in levels:
        return 70

    return 100 if levels.index(user_level) >= levels.index(required_level) else 40


def education_match(user_education, required_education):
    if not required_education:
        return 100

    return 100 if required_education.lower() in user_education.lower() else 50


def responsibility_match(user_projects, responsibilities):
    if not responsibilities:
        return 80

    hits = sum(
        1 for r in responsibilities
        if any(word.lower() in user_projects.lower() for word in r.split())
    )

    return min(100, hits * 20)
