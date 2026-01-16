import re

ACTION_VERBS = [
    "developed", "built", "designed", "implemented", "created",
    "analyzed", "managed", "led", "optimized", "improved"
]

KEYWORDS = [
    "python", "sql", "java", "ai", "machine learning",
    "data", "streamlit", "power bi", "excel"
]


def score_resume(resume_text: str):
    text = resume_text.lower()

    # -------------------------------
    # 1. COMPLETENESS (25%)
    # -------------------------------
    sections = {
        "contact": ["email", "phone"],
        "summary": ["summary", "objective"],
        "experience": ["experience", "internship", "project"],
        "education": ["education", "degree"],
        "skills": ["skills"]
    }

    present_sections = sum(
        any(k in text for k in keys)
        for keys in sections.values()
    )

    completeness_score = round((present_sections / 5) * 25, 2)

    completeness_reason = f"{present_sections}/5 essential sections found"

    # -------------------------------
    # 2. CONTENT QUALITY (30%)
    # -------------------------------
    verb_count = sum(text.count(v) for v in ACTION_VERBS)
    number_count = len(re.findall(r"\d+", text))

    content_score = min(verb_count * 3 + number_count * 2, 30)

    content_reason = "Uses action verbs and quantifiable details"

    # -------------------------------
    # 3. FORMATTING (15%)
    # -------------------------------
    length = len(text.split())

    if 300 <= length <= 900:
        formatting_score = 15
        formatting_reason = "Appropriate resume length"
    elif 200 <= length < 300 or 900 < length <= 1200:
        formatting_score = 10
        formatting_reason = "Acceptable length"
    else:
        formatting_score = 5
        formatting_reason = "Poor length or readability"

    # -------------------------------
    # 4. KEYWORD RELEVANCE (20%)
    # -------------------------------
    keyword_hits = sum(1 for k in KEYWORDS if k in text)
    keyword_score = min(keyword_hits * 3, 20)

    keyword_reason = f"{keyword_hits} industry keywords found"

    # -------------------------------
    # 5. EXPERIENCE (10%)
    # -------------------------------
    years = len(re.findall(r"\d+\s+year", text))

    if years >= 3:
        experience_score = 10
    elif years == 2:
        experience_score = 7
    elif years == 1:
        experience_score = 5
    else:
        experience_score = 3

    experience_reason = "Experience inferred from resume text"

    # -------------------------------
    # FINAL SCORE
    # -------------------------------
    final_score = round(
        completeness_score +
        content_score +
        formatting_score +
        keyword_score +
        experience_score,
        2
    )

    if final_score >= 90:
        grade = "Excellent"
    elif final_score >= 75:
        grade = "Good"
    elif final_score >= 60:
        grade = "Average"
    else:
        grade = "Needs Improvement"

    return {
        "final_score": final_score,
        "grade": grade,
        "breakdown": {
            "completeness": {
                "score": completeness_score,
                "reason": completeness_reason
            },
            "content_quality": {
                "score": content_score,
                "reason": content_reason
            },
            "formatting": {
                "score": formatting_score,
                "reason": formatting_reason
            },
            "keyword_relevance": {
                "score": keyword_score,
                "reason": keyword_reason
            },
            "experience": {
                "score": experience_score,
                "reason": experience_reason
            }
        }
    }
