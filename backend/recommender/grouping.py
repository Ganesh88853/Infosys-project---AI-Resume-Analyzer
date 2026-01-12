from datetime import datetime, timedelta

def group_jobs(ranked_jobs):
    """
    Groups ranked jobs into frontend-ready sections
    """

    result = {
        "best_matches": [],
        "featured": [],
        "excellent": [],
        "good": [],
        "fair": [],
        "stats": {
            "total_jobs": len(ranked_jobs),
            "new_today": 0,
            "average_match": 0
        }
    }

    today = datetime.now().date()
    match_sum = 0

    for job in ranked_jobs:
        match = job.get("match_score", 0)
        match_sum += match

        # New jobs today
        posted = job.get("posted_date")
        if posted and hasattr(posted, "date") and posted.date() == today:
            result["stats"]["new_today"] += 1

        # Featured jobs
        if job.get("featured"):
            result["featured"].append(job)

        # Match bands
        if match >= 85:
            result["excellent"].append(job)
        elif 70 <= match <= 84:
            result["good"].append(job)
        elif 60 <= match <= 69:
            result["fair"].append(job)

    # Best matches = top 10 ranked jobs
    result["best_matches"] = ranked_jobs[:10]

    # Average match score
    if ranked_jobs:
        result["stats"]["average_match"] = round(
            match_sum / len(ranked_jobs), 2
        )

    return result
