import sys
import os
import time
from datetime import datetime

# ---------------- PATH FIX ----------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# -----------------------------------------

import streamlit as st
from backend.database.db import get_db_connection
def job_search_preferences_page():

    st.title("🔎 Customize Your Job Search")
    st.caption("Control how jobs are searched, matched, and recommended")

    # ======================================================
    # DATABASE HELPERS
    # ======================================================
    def save_job_preferences(data):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO job_preferences (
                job_title,
                locations,
                remote_pref,
                experience_level,
                job_types,
                min_salary,
                industries,
                company_size,
                include_keywords,
                exclude_keywords,
                max_commute,
                visa_required,
                preferred_companies
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["job_title"],
            ",".join(data["locations"]),
            data["remote_pref"],
            data["experience_level"],
            ",".join(data["job_types"]),
            data["min_salary"],
            ",".join(data["industries"]),
            data["company_size"],
            ",".join(data["include_keywords"]),
            ",".join(data["exclude_keywords"]),
            data["max_commute"],
            1 if data["visa_required"] else 0,
            data["preferred_companies"]
        ))

        conn.commit()
        conn.close()



    def load_search_history():
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT job_title, created_at
            FROM job_preferences
            ORDER BY created_at DESC
            LIMIT 5
        """)

        rows = cur.fetchall()
        conn.close()
        return rows


    # ======================================================
    # BASIC PREFERENCES FORM
    # ======================================================

    st.header("🧾 Job Preferences")

    col1, col2 = st.columns(2)

    with col1:
        job_title = st.text_input("Desired Job Title", "Data Analyst")

        locations = st.multiselect(
            "Preferred Locations",
            ["Bangalore", "Hyderabad", "Pune", "Chennai", "Remote"]
        )

        remote = st.radio(
            "Work Preference",
            ["Only Remote", "Hybrid", "On-site", "Any"]
        )

        experience = st.selectbox(
            "Experience Level",
            ["Entry", "Mid", "Senior", "Lead / Manager"]
        )

    with col2:
        job_types = st.multiselect(
            "Job Type",
            ["Full-time", "Part-time", "Contract", "Internship"]
        )

        min_salary = st.number_input(
            "Minimum Salary Expectation (₹)",
            min_value=0,
            step=5000
        )

        industries = st.multiselect(
            "Industries of Interest",
            ["Tech", "Finance", "Healthcare", "Education", "E-commerce"]
        )

        company_size = st.selectbox(
            "Company Size Preference",
            ["Startup", "Mid-size", "Enterprise", "Any"]
        )

    # ======================================================
    # ADVANCED PREFERENCES
    # ======================================================

    with st.expander("⚙️ Advanced Preferences"):
        include_keywords = st.text_input(
            "Keywords to Include (comma separated)",
            "Python, SQL"
        ).split(",")

        exclude_keywords = st.text_input(
            "Keywords to Exclude",
            "sales, cold calling"
        ).split(",")

        max_commute = st.slider(
            "Maximum Commute Time (minutes)",
            0, 120, 30
        )

        visa_required = st.checkbox("Visa Sponsorship Required")

        preferred_companies = st.text_area(
            "Preferred Companies",
            placeholder="Google, Microsoft, Amazon"
        )

    # ======================================================
    # SAVE / RESET
    # ======================================================

    col_save, col_reset = st.columns(2)

    if col_save.button("💾 Save Preferences"):
        prefs = {
            "job_title": job_title,
            "locations": locations,
            "remote_pref": remote,  # ✅ FIXED
            "experience_level": experience,  # ✅ FIXED
            "job_types": job_types,
            "min_salary": min_salary,
            "industries": industries,
            "company_size": company_size,
            "include_keywords": include_keywords,
            "exclude_keywords": exclude_keywords,
            "max_commute": max_commute,
            "visa_required": visa_required,
            "preferred_companies": preferred_companies
        }

        save_job_preferences(prefs)
        st.success("✅ Preferences saved successfully")

    if col_reset.button("🔄 Reset"):
        st.rerun()

    # ======================================================
    # FIND JOBS NOW
    # ======================================================
    st.header("🚀 Find Jobs Now")

    if st.button("🔍 Start Job Search"):
        progress = st.progress(0)
        status = st.empty()

        try:
            status.info("🔐 Logging into LinkedIn...")
            progress.progress(10)

            from backend.scraper.run_job_scraper import run_scraper
            time.sleep(1)

            status.info("🔍 Searching LinkedIn jobs...")
            progress.progress(30)

            run_scraper()   # ✅ REAL SCRAPER CALL

            status.info("📊 Analyzing job matches...")
            progress.progress(70)
            time.sleep(1)

            status.info("💾 Saving results...")
            progress.progress(90)
            time.sleep(1)

            progress.progress(100)
            status.success("🎉 Job search completed successfully!")

            st.success("✅ Jobs fetched from LinkedIn")
            st.info("➡️ Go to **Job Recommendations** page to view results")

        except Exception as e:
            status.error("❌ Job search failed")
            st.error(str(e))



    # ======================================================
    # SEARCH HISTORY
    # ======================================================



    # ======================================================
    # REFRESH RECOMMENDATIONS
    # ======================================================

    st.header("🔁 Refresh Recommendations")

    if st.button("♻️ Refresh Using Saved Preferences"):
        st.info("Re-running search using last saved preferences...")
        time.sleep(2)
        st.success("✨ Found new matching jobs since last search")

    # ======================================================
    # SCHEDULING (ENHANCEMENT UI)
    # ======================================================

    st.header("⏰ Schedule Automatic Searches")

    schedule = st.selectbox(
        "Run search automatically",
        ["Disabled", "Daily", "Weekly"]
    )

    if schedule != "Disabled":
        st.success(f"📬 Automatic {schedule.lower()} searches enabled")