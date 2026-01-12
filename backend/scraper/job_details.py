from selenium.webdriver.common.by import By
import time

from backend.jobs.job_normalizer import (
    normalize_posted_date,
    detect_job_type,
    detect_experience_level,
    detect_remote
)


def extract_job_details(driver, job_url):
    print(f"🔗 Opening job: {job_url}")
    driver.get(job_url)
    time.sleep(4)

    def safe_text(by, value):
        try:
            return driver.find_element(by, value).text.strip()
        except:
            return ""

    # ✅ Extract posted text properly
    posted_text = safe_text(
        By.CSS_SELECTOR,
        ".jobs-unified-top-card__posted-date"
    )

    job = {
        "url": job_url,
        "title": safe_text(By.CSS_SELECTOR, "h1"),
        "company": safe_text(By.CSS_SELECTOR, ".jobs-unified-top-card__company-name"),
        "location": safe_text(By.CSS_SELECTOR, ".jobs-unified-top-card__bullet"),
        "description": safe_text(By.CSS_SELECTOR, ".jobs-description__content"),
        "posted_text": posted_text
    }

    # ✅ Normalization (Task-15 requirement)
    job["job_type"] = detect_job_type(job["description"])
    job["experience_level"] = detect_experience_level(job["description"])
    job["remote"] = detect_remote(job["location"], job["description"])
    job["posted_date"] = normalize_posted_date(posted_text)

    return job
