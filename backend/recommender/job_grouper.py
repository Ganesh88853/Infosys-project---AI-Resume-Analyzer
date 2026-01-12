def group_jobs_by_match(jobs):
    groups = {
        "excellent": [],
        "good": [],
        "fair": []
    }

    for job in jobs:
        score = job.get("match_score", 0)

        if score >= 85:
            groups["excellent"].append(job)
        elif score >= 70:
            groups["good"].append(job)
        elif score >= 60:
            groups["fair"].append(job)

    return groups
