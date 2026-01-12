# backend/matching/job_filter.py

def filter_jobs(
    jobs,
    min_match_percentage=60,
    preferred_locations=None,
    allow_remote=True
):
    """
    Filters jobs based on relevance rules

    jobs: list of job dicts (already having match_score)
    """

    filtered_jobs = []

    for job in jobs:
        # 1️⃣ Match score threshold
        if job["match_score"] < min_match_percentage:
            continue

        # 2️⃣ Location filtering
        if preferred_locations:
            if job.get("remote") and allow_remote:
                pass
            elif job.get("location") not in preferred_locations:
                continue

        filtered_jobs.append(job)

    return filtered_jobs
