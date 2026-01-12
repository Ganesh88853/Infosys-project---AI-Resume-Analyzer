def generate_application_tips(job, resume_skills):
    """
    Fallback application tips generator (no LLM).
    Works reliably for Task 17 + frontend.
    """

    job_title = job.get("title", "").lower()
    job_desc = job.get("description", "").lower()

    resume_skills = set([s.lower() for s in resume_skills])

    # Common skill keywords by role
    role_skill_map = {
        "data analyst": ["sql", "excel", "python", "power bi", "tableau", "statistics"],
        "ml engineer": ["python", "machine learning", "deep learning", "tensorflow", "pytorch"],
        "software engineer": ["python", "java", "javascript", "data structures", "algorithms"],
    }

    required_skills = []
    for role, skills in role_skill_map.items():
        if role in job_title:
            required_skills = skills
            break

    matching_skills = [s for s in required_skills if s in resume_skills]
    missing_skills = [s for s in required_skills if s not in resume_skills]

    tips = {
        "skills_to_highlight": matching_skills,
        "missing_skills": missing_skills,
        "cover_letter_tips": [],
        "interview_talking_points": [],
        "resume_keywords_to_add": missing_skills,
    }

    # Cover letter tips
    if matching_skills:
        tips["cover_letter_tips"].append(
            f"Emphasize your hands-on experience with {', '.join(matching_skills)}."
        )

    if missing_skills:
        tips["cover_letter_tips"].append(
            f"Show willingness to learn {', '.join(missing_skills)} quickly."
        )

    # Interview talking points
    tips["interview_talking_points"].append(
        "Be ready to explain real projects you worked on."
    )
    tips["interview_talking_points"].append(
        "Explain how your past work solves business problems."
    )

    # Job-type specific tips
    if job.get("remote"):
        tips["interview_talking_points"].append(
            "Highlight your ability to work independently in remote setups."
        )

    return tips
