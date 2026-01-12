import sys
import os

# ---------- FORCE PROJECT ROOT INTO PYTHON PATH ----------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# --------------------------------------------------------


import streamlit as st
from datetime import date
from backend.database.db import get_db_connection
from backend.recommender.recommendation_engine import generate_recommendations

st.set_page_config(
    page_title="Job Recommendations",
    layout="wide"
)

# ======================================================
# DATABASE QUERY (CORRECT & FINAL)
# ======================================================

def load_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            j.id,
            j.job_title,
            j.company,
            j.location,
            j.job_url,
            j.description,
            j.posted_date,
            j.job_type,
            j.experience_level,

            COALESCE(jm.match_score, 0),
            COALESCE(jm.skill_match, 0),
            COALESCE(jm.experience_match, 0),
            COALESCE(jm.education_match, 0),
            COALESCE(jm.responsibility_match, 0),
            jm.match_reason,
            jm.application_status

        FROM jobs j
        LEFT JOIN job_matches jm ON jm.job_id = j.id
        ORDER BY jm.match_score DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    jobs = []
    for r in rows:
        jobs.append({
            "id": r[0],
            "job_title": r[1],
            "company": r[2],
            "location": r[3],
            "job_url": r[4],
            "description": r[5],
            "posted_date": r[6],
            "job_type": r[7],
            "experience_level": r[8],
            "match_score": r[9],
            "skill_match": r[10],
            "experience_match": r[11],
            "education_match": r[12],
            "responsibility_match": r[13],
            "match_reason": r[14],
            "application_status": r[15]
        })

    return jobs


# ======================================================
# SUMMARY SECTION
# ======================================================

def render_summary(jobs):
    total_jobs = len(jobs)

    avg_match = round(
        sum(j["match_score"] for j in jobs) / total_jobs,
        1
    ) if total_jobs else 0

    today = date.today().isoformat()
    new_today = len([j for j in jobs if j["posted_date"] == today])

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Total Jobs", total_jobs)
    col2.metric("🎯 Avg Match %", avg_match)
    col3.metric("🆕 New Jobs Today", new_today)


# ======================================================
# SIDEBAR FILTERS
# ======================================================

def sidebar_filters():
    st.sidebar.header("🔍 Filters")

    min_match = st.sidebar.slider("Minimum Match %", 0, 100, 60)

    job_type = st.sidebar.multiselect(
        "Job Type",
        ["Full-time", "Part-time", "Contract", "Internship"]
    )

    experience = st.sidebar.multiselect(
        "Experience Level",
        ["Entry", "Mid", "Senior"]
    )

    location = st.sidebar.text_input("Location contains")

    sort_by = st.sidebar.selectbox(
        "Sort By",
        ["Best Match", "Most Recent"]
    )

    return min_match, job_type, experience, location, sort_by


# ======================================================
# FILTER + SORT LOGIC
# ======================================================

def apply_filters(jobs, min_match, job_type, experience, location, sort_by):
    filtered = []

    for job in jobs:
        if job["match_score"] < min_match:
            continue
        if job_type and job["job_type"] not in job_type:
            continue
        if experience and job["experience_level"] not in experience:
            continue
        if location and location.lower() not in job["location"].lower():
            continue
        filtered.append(job)

    if sort_by == "Best Match":
        filtered.sort(key=lambda x: x["match_score"], reverse=True)
    else:
        filtered.sort(key=lambda x: x["posted_date"], reverse=True)

    return filtered


# ======================================================
# JOB CARD UI
# ======================================================

def match_color(score):
    if score >= 85:
        return "🟢"
    elif score >= 70:
        return "🟡"
    else:
        return "🟠"


def render_job_card(job):
    st.markdown("---")
    col1, col2 = st.columns([4, 1])

    with col1:
        st.subheader(job["job_title"])
        st.write(f"🏢 **{job['company']}**")
        st.write(f"📍 {job['location']}")
        st.write(
            f"{match_color(job['match_score'])} "
            f"**Match: {job['match_score']}%**"
        )

        with st.expander("📋 View Details"):
            st.write(job["description"])

            st.markdown("**Match Breakdown**")
            st.progress(job["skill_match"] / 100)
            st.caption(f"Skills Match: {job['skill_match']}%")

            st.progress(job["experience_match"] / 100)
            st.caption(f"Experience Match: {job['experience_match']}%")

            st.progress(job["education_match"] / 100)
            st.caption(f"Education Match: {job['education_match']}%")

            st.progress(job["responsibility_match"] / 100)
            st.caption(f"Responsibilities Match: {job['responsibility_match']}%")

            if job["match_reason"]:
                st.info(job["match_reason"])

    with col2:
        st.link_button("🔗 Apply", job["job_url"])
        st.write(f"Status: {job['application_status'] or 'Not Applied'}")


# ======================================================
# EMPTY STATE
# ======================================================

def empty_state():
    st.warning("😕 No jobs found")
    st.info("Try lowering match threshold or adjusting filters")


# ======================================================
# MAIN PAGE
# ======================================================

st.title("💼 Job Recommendations")
st.caption("Personalized job matches based on your profile")

jobs = load_jobs()

if not jobs:
    empty_state()
    st.stop()

# 🔥 STEP 1: USE RECOMMENDER ENGINE
recommendations = generate_recommendations(jobs)

ranked_jobs = recommendations["ranked_jobs"]

# 🔥 STEP 2: SUMMARY BASED ON RANKED JOBS
render_summary(ranked_jobs)

# 🔥 STEP 3: FILTERS
min_match, job_type, experience, location, sort_by = sidebar_filters()

filtered_jobs = apply_filters(
    ranked_jobs,
    min_match,
    job_type,
    experience,
    location,
    sort_by
)

# 🔥 STEP 4: DISPLAY
st.header("🔥 Best Matches")

if not filtered_jobs:
    empty_state()
else:
    for job in filtered_jobs[:10]:
        render_job_card(job)
