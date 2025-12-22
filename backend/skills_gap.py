# backend/skills_gap.py

"""
Industry skill standards for different roles
This avoids LLM failures and makes project stable
"""

ROLE_SKILLS = {
    "data_analyst": {
        "critical": [
            "Python",
            "SQL",
            "Data Analysis",
            "Statistics",
            "Excel"
        ],
        "nice_to_have": [
            "Power BI",
            "Tableau",
            "Machine Learning",
            "Pandas",
            "NumPy"
        ]
    },

    "ai_intern": {
        "critical": [
            "Python",
            "Machine Learning",
            "AI",
            "Data Structures"
        ],
        "nice_to_have": [
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "Statistics"
        ]
    },

    "software_developer": {
        "critical": [
            "Python",
            "Java",
            "Data Structures",
            "Algorithms"
        ],
        "nice_to_have": [
            "Spring Boot",
            "Docker",
            "Git",
            "SQL"
        ]
    }
}

def flatten_extracted_skills(extracted_skills: dict) -> set:
    """
    Converts extracted skills JSON into a flat set of skill names
    """
    flat_skills = set()

    tech = extracted_skills.get("technical_skills", {})

    for category in ["programming_languages", "frameworks", "tools", "domain_knowledge"]:
        for skill in tech.get(category, []):
            flat_skills.add(skill["name"].lower())

    for skill in extracted_skills.get("soft_skills", []):
        flat_skills.add(skill.lower())

    for cert in extracted_skills.get("certifications", []):
        flat_skills.add(cert.lower())

    return flat_skills




def analyze_skill_gap(extracted_skills: dict, target_role: str):
    """
    Compare resume skills with industry-required skills
    """

    if target_role not in ROLE_SKILLS:
        raise ValueError("Unsupported role")

    role_data = ROLE_SKILLS[target_role]

    resume_skills = flatten_extracted_skills(extracted_skills)

    critical_missing = []
    nice_to_have_missing = []

    for skill in role_data["critical"]:
        if skill.lower() not in resume_skills:
            critical_missing.append(skill)

    for skill in role_data["nice_to_have"]:
        if skill.lower() not in resume_skills:
            nice_to_have_missing.append(skill)

    recommendations = []

    for skill in critical_missing + nice_to_have_missing:
        recommendations.append({
            "skill": skill,
            "importance": "High" if skill in critical_missing else "Medium",
            "why": f"{skill} is commonly required for {target_role.replace('_',' ').title()} roles",
            "use_cases": f"Used in real-world {target_role.replace('_',' ')} projects",
            "resources": [
                "Coursera",
                "YouTube",
                "Official Documentation"
            ]
        })

    return {
        "target_role": target_role,
        "present_skills": list(resume_skills),
        "missing_critical_skills": critical_missing,
        "missing_nice_to_have_skills": nice_to_have_missing,
        "recommendations": recommendations[:10]  # limit to 10
    }
