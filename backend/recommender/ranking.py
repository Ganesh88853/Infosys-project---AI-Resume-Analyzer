from datetime import datetime, timedelta

# ----------------------------
# CONFIG (easy to tune later)
# ----------------------------
REMOTE_BONUS = 10
LOW_APPLICANTS_BONUS = 10
SALARY_MATCH_BONUS = 10
RECENT_JOB_BONUS = 5
FEATURED_THRESHOLD = 90

LOW_APPLICANTS_LIMIT = 20


def calculate_ranking_score(job, user_preferences=None):
    """
    Calculates final ranking score using weighted bonuses
    """

    score = job.get("match_score", 0)

    # Remote / Hybrid preference
    if job.get("remote"):
        score += REMOTE_BONUS

    # Fewer applicants → higher chance
    applicants = job.get("applicants", None)
    if applicants is not None and applicants <= LOW_APPLICANTS_LIMIT:
        score += LOW_APPLICANTS_BONUS

    # Salary alignment
    if user_preferences and job.get("salary"):
        min_salary = user_preferences.get("min_salary")
        if min_salary and job["salary"] >= min_salary:
            score += SALARY_MATCH_BONUS

    # Recent jobs bonus (last 24 hours)
    posted_date = job.get("posted_date")
    if posted_date:
        if isinstance(posted_date, datetime):
            if posted_date >= datetime.now() - timedelta(days=1):
                score += RECENT_JOB_BONUS

    return round(score, 2)


def apply_priority(job):
    """
    Determines application priority
    """
    if job["match_score"] >= 85 and job.get("applicants", 999) <= 20:
        return "Apply First"

    if job["match_score"] >= 70:
        return "Apply Soon"

    return "Can Wait"


def is_featured(job):
    """
    Featured job logic
    """
    if job["match_score"] >= FEATURED_THRESHOLD:
        return True

    posted_date = job.get("posted_date")
    if posted_date and isinstance(posted_date, datetime):
        return posted_date >= datetime.now() - timedelta(days=1)

    return False


def rank_jobs(jobs, user_preferences=None):
    """
    Main ranking function used by frontend
    """

    ranked_jobs = []

    for job in jobs:
        job["ranking_score"] = calculate_ranking_score(job, user_preferences)
        job["priority"] = apply_priority(job)
        job["featured"] = is_featured(job)

        ranked_jobs.append(job)

    # PRIMARY SORT: ranking_score
    # SECONDARY SORT: posted_date
    ranked_jobs.sort(
        key=lambda x: (
            x["ranking_score"],
            x.get("posted_date") or datetime.min
        ),
        reverse=True
    )

    return ranked_jobs
