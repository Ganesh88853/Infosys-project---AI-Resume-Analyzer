import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.recommender.application_tips import generate_application_tips

job = {
    "title": "Data Analyst Intern",
    "description": "Looking for SQL and Python skills",
    "remote": True
}

resume_skills = ["python", "excel"]

print(generate_application_tips(job, resume_skills))
