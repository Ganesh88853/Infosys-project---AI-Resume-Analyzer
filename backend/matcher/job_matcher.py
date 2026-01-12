from backend.matcher.resume_job_matcher import (
    calculate_skill_match,
    experience_match,
    education_match,
    responsibility_match
)

def calculate_overall_match(user_profile, job_req):
    skill_score = calculate_skill_match(
        user_profile["skills"],
        job_req["must_have_skills"]
    )

    exp_score = experience_match(
        user_profile["experience_level"],
        job_req["seniority_level"]
    )

    edu_score = education_match(
        user_profile["education"],
        job_req["required_education"]
    )

    resp_score = responsibility_match(
        user_profile["projects"],
        job_req["responsibilities"]
    )

    final_score = (
        skill_score * 0.50 +
        exp_score * 0.25 +
        edu_score * 0.15 +
        resp_score * 0.10
    )

    return round(final_score, 2)
