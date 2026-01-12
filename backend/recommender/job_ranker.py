def rank_jobs(jobs):
    return sorted(
        jobs,
        key=lambda j: (
            -j.get("match_score", 0),
            -j.get("priority_score", 0),
            j.get("posted_date")
        )
    )
