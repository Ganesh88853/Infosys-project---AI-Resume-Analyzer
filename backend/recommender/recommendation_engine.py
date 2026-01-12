from backend.recommender.job_ranker import rank_jobs
from backend.recommender.job_grouper import group_jobs_by_match
from backend.recommender.priority_engine import compute_priority

def generate_recommendations(jobs):
    for job in jobs:
        compute_priority(job)

    ranked = rank_jobs(jobs)
    grouped = group_jobs_by_match(ranked)

    return {
        "summary": {
            "total_jobs": len(jobs),
            "best_matches": len(grouped["excellent"])
        },
        "grouped_jobs": grouped,
        "ranked_jobs": ranked[:20]  # Top 20
    }
