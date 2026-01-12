import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from backend.recommender.ranking import rank_jobs
from backend.recommender.grouping import group_jobs
from datetime import datetime

jobs = [
    {
        "title": "Data Analyst",
        "match_score": 88,
        "featured": True,
        "remote": True,
        "posted_date": datetime.now()
    },
    {
        "title": "ML Engineer",
        "match_score": 72,
        "featured": False,
        "remote": False,
        "posted_date": datetime.now()
    },
    {
        "title": "Intern",
        "match_score": 65,
        "featured": False,
        "remote": True,
        "posted_date": datetime.now()
    }
]

ranked = rank_jobs(jobs)
grouped = group_jobs(ranked)

print("BEST:", len(grouped["best_matches"]))
print("EXCELLENT:", len(grouped["excellent"]))
print("GOOD:", len(grouped["good"]))
print("FAIR:", len(grouped["fair"]))
print("STATS:", grouped["stats"])
