import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.recommender.recommendation_engine import generate_recommendations

jobs = [
    {"title": "Data Analyst", "match_score": 88, "posted_date": None},
    {"title": "ML Engineer", "match_score": 72, "posted_date": None},
    {"title": "Intern", "match_score": 61, "posted_date": None},
]

result = generate_recommendations(jobs)

print("SUMMARY:", result["summary"])
print("EXCELLENT:", len(result["grouped_jobs"]["excellent"]))
print("GOOD:", len(result["grouped_jobs"]["good"]))
print("FAIR:", len(result["grouped_jobs"]["fair"]))
