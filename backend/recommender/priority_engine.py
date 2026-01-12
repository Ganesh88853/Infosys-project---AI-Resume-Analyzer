from datetime import datetime, timedelta

def compute_priority(job):
    score = job.get("match_score", 0)
    posted_date = job.get("posted_date")

    priority = 0

    # Match score weight
    priority += score * 0.6

    # Recency boost
    if posted_date:
        days_old = (datetime.now().date() - posted_date).days
        if days_old <= 1:
            priority += 20
        elif days_old <= 3:
            priority += 10

    job["priority_score"] = round(priority, 2)
    job["apply_first"] = priority >= 80

    return job
