


def generate_improvement_suggestions(resume_text, weaknesses):
    """
    GUARANTEED improvement generator
    This function NEVER returns empty output
    """

    suggestions = []

    # -------------------------
    # RULE 1: WEAKNESSES BASED
    # -------------------------
    if weaknesses:
        for w in weaknesses:
            suggestions.append({
                "title": f"Improve {w.get('category', 'resume section')}",
                "description": f"Address the issue: {w.get('point', 'Improve clarity and impact')}",
                "priority": "high" if w.get("severity") == "critical" else "medium",
                "estimated_score_improvement": 8,
                "before": w.get("example", "Responsibility listed without impact."),
                "after": "Rewritten using strong action verbs and measurable outcomes."
            })

    # -------------------------
    # RULE 2: ALWAYS ADD CORE IMPROVEMENTS
    # -------------------------
    suggestions.extend([
        {
            "title": "Add measurable achievements",
            "description": "Quantify your work using numbers (%, time saved, accuracy, users impacted).",
            "priority": "high",
            "estimated_score_improvement": 10,
            "before": "Worked on a machine learning project.",
            "after": "Built a machine learning model achieving 92% accuracy on test data."
        },
        {
            "title": "Improve resume summary",
            "description": "Start with your strongest skill, role, and impact in 2–3 lines.",
            "priority": "medium",
            "estimated_score_improvement": 6,
            "before": "I am a student interested in AI.",
            "after": "AI-focused Computer Science student with hands-on experience in ML models and data analysis."
        },
        {
            "title": "Optimize skills section for ATS",
            "description": "Group skills into categories like Programming, Tools, Frameworks.",
            "priority": "medium",
            "estimated_score_improvement": 5,
            "before": "Python, SQL, AI, Git",
            "after": "Programming: Python, SQL | Tools: Git, Streamlit | Domain: AI, ML"
        }
    ])

    # -------------------------
    # FINAL GUARANTEE
    # -------------------------
    return {
        "suggestions": suggestions
    }