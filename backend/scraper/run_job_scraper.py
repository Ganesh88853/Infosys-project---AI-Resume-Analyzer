import sys
import os
import json

# ---------------- PATH FIX ----------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ------------------------------------------

from backend.scraper.driver_manager import get_driver
from backend.scraper.linkedin_login import login_linkedin
from backend.scraper.job_search import search_jobs, extract_job_cards
from backend.scraper.job_details import extract_job_details

from backend.jobs.job_repository import save_job
from backend.database.match_repository import save_job_match
from backend.preferences.preference_repository import get_latest_preferences

from backend.matcher.job_requirement_extractor import extract_job_requirements
from backend.matcher.job_matcher import calculate_overall_match
from backend.matcher.match_explainer import generate_match_explanation

# --------------------------------------------------
# TEMP USER PROFILE (UNTIL RESUME PARSER IS READY)
# --------------------------------------------------
def get_user_profile():
    return {
        "skills": ["python", "sql", "data analysis", "machine learning"],
        "experience_level": "mid",
        "education": "bachelor of technology in computer science",
        "projects": "data analytics project using python and sql"
    }


def run_scraper(max_pages=3):
    driver = get_driver()
    user_id = 1  # single user for now

    try:
        #1️⃣ LOGIN
        login_linkedin(driver)

        # 2️⃣ LOAD USER PREFERENCES
        prefs = get_latest_preferences()
        if not prefs:
            raise RuntimeError("❌ No job preferences found. Save preferences first.")

        job_title = prefs["job_title"]
        locations = prefs["locations"] or ["India"]

        print(f"🎯 Preferences loaded: {job_title} | {locations}")

        user_profile = get_user_profile()

        # 3️⃣ SEARCH JOBS
        for location in locations:
            print(f"\n🔍 Searching jobs: {job_title} in {location}")
            search_jobs(driver, job_title, location)

            job_links = extract_job_cards(driver, max_pages=max_pages)
            print(f"🔗 Job links collected: {len(job_links)}")

            for link in job_links:
                job = extract_job_details(driver, link)
                if not job:
                    continue

                # 4️⃣ SAVE JOB
                job_id = save_job(job)
                if job_id == "duplicate":
                    continue

                # 5️⃣ EXTRACT JOB REQUIREMENTS (LLM)
                job_req = extract_job_requirements(job["description"])

                # 6️⃣ CALCULATE MATCH SCORE
                match_score = calculate_overall_match(
                    user_profile,
                    job_req
                )

                # 7️⃣ GENERATE MATCH EXPLANATION
                explanation = generate_match_explanation(
                    job,
                    job_req,
                    user_profile
                )

                # 8️⃣ SAVE MATCH RESULT
                save_job_match(
                    job_id=job_id,
                    user_id=user_id,
                    score=match_score,
                    explanation=json.dumps(explanation)
                )

                print(f"✅ Job matched | Score: {match_score}%")

        print("\n🎉 Scraping + Matching completed successfully")

    finally:
        driver.quit()
        print("🛑 Browser closed safely")


if __name__ == "__main__":
    run_scraper()
