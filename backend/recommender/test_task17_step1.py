import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from backend.recommender.ranking import rank_jobs
from datetime import datetime

jobs = [
    {
        "title": "Data Analyst",
        "match_score": 82,
        "remote": True,
        "applicants": 15,
        "posted_date": datetime.now()
    },
    {
        "title": "ML Engineer",
        "match_score": 75,
        "remote": False,
        "applicants": 80,
        "posted_date": datetime.now()
    }
]

ranked = rank_jobs(jobs)

for j in ranked:
    print(j["title"], j["ranking_score"], j["priority"], j["featured"])
