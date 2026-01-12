import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.matcher.job_filter import filter_jobs

# 🔹 Mock scored jobs (simulate output from Task 15 + scoring)
mock_jobs = [
    {
        "title": "Data Analyst",
        "location": "Bangalore",
        "remote": False,
        "match_score": 82
    },
    {
        "title": "ML Engineer",
        "location": "Remote",
        "remote": True,
        "match_score": 91
    },
    {
        "title": "Junior Tester",
        "location": "Hyderabad",
        "remote": False,
        "match_score": 45
    }
]

# 🔹 Apply filtering (Task 16)
filtered_jobs = filter_jobs(
    jobs=mock_jobs,
    min_match_percentage=60,
    preferred_locations=["Bangalore", "Remote"],
    allow_remote=True
)

print("✅ FILTERED JOBS:")
for job in filtered_jobs:
    print(job["title"], "-", job["match_score"])
