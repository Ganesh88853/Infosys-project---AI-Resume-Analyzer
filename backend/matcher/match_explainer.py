def generate_match_explanation(job, job_req, user_profile):
    matched = set(user_profile["skills"]) & set(job_req["must_have_skills"])
    missing = set(job_req["must_have_skills"]) - set(user_profile["skills"])

    explanation = {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "reason": f"Matched {len(matched)} required skills. "
                  f"Experience level aligns with {job_req['seniority_level']} role."
    }

    return explanation
