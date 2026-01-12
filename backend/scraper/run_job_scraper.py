import sys
import os
import json

# ---------------- PATH FIX ----------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.scraper.driver_manager import get_driver
from backend.scraper.linkedin_login import login_linkedin
from backend.scraper.job_search import search_jobs, extract_job_cards
from backend.scraper.job_details import extract_job_details   # ✅ IMPORT
from backend.jobs.job_repository import save_job
def run_scraper():
    driver = get_driver()
    job_data = []   # ✅ ADD THIS

    try:
        login_linkedin(driver)

        search_jobs(
            driver,
            job_title="Data Analyst",
            location="Bangalore"
        )

        job_links = extract_job_cards(driver, max_pages=3)
        print(f"\n🔗 Job links collected: {len(job_links)}")

        # ✅ ADD THIS BLOCK
        for link in job_links:
            details = extract_job_details(driver, link)
            job_data.append(details)

        print(f"\n✅ Final jobs extracted: {len(job_data)}")

        saved = 0
        duplicates = 0

        for job in job_data:
            result = save_job(job)

            if result == "saved":
                saved += 1
            elif result == "duplicate":
                duplicates += 1

        print(f"💾 Jobs saved: {saved}")
        print(f"🔁 Duplicates skipped: {duplicates}")

        # OPTIONAL: print one job to verify
        if job_data:
            print("\n🧪 SAMPLE JOB:\n", job_data[0])

    finally:
        driver.quit()
        print("🛑 Browser closed safely")

if __name__ == "__main__":
    run_scraper()
