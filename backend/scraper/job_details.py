# backend/scraper/job_details.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from backend.scraper.utils import random_delay


def extract_job_details(driver, job_url):
    """
    Open a LinkedIn job page and extract detailed job info
    """

    print(f"🔗 Opening job: {job_url}")
    driver.get(job_url)

    wait = WebDriverWait(driver, 25)

    # Wait until job description section loads
    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.jobs-description-content")
            )
        )
    except:
        print("⚠️ Job description not fully loaded")

    random_delay(2, 4)

    # -----------------------------
    # SAFE EXTRACTIONS
    # -----------------------------
    def safe_text(selector):
        try:
            return driver.find_element(By.CSS_SELECTOR, selector).text.strip()
        except:
            return ""

    title = safe_text("h1")
    company = safe_text("a.topcard__org-name-link, span.jobs-unified-top-card__company-name")
    location = safe_text("span.jobs-unified-top-card__bullet")
    description = safe_text("div.jobs-description-content")

    job_data = {
        "title": title,
        "company": company,
        "location": location,
        "description": description,
        "url": job_url,
        "employment_type": None,   # optional – can be filled later
    }

    return job_data
