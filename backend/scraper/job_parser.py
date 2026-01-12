import time
from selenium.webdriver.common.by import By
from backend.scraper.job_details import parse_posted_date
def extract_job_details(driver, job):
    driver.get(job["url"])
    time.sleep(5)

    try:
        description = driver.find_element(
            By.CSS_SELECTOR, "div.jobs-description"
        ).text
    except Exception:
        description = ""

    job["description"] = description

    try:
        posted_text = driver.find_element(
            By.CSS_SELECTOR,
            "span.posted-time-ago__text"
        ).text
    except:
        posted_text = None

    posted_date = parse_posted_date(posted_text)

    return job
