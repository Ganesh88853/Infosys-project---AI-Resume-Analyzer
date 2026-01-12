def compare_jobs(jobs):
    comparison = []

    for job in jobs:
        comparison.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "match_score": job["match_score"],
            "job_type": job.get("job_type"),
            "experience_level": job.get("experience_level")
        })

    return comparison
