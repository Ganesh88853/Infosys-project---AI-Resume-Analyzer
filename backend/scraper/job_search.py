from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from backend.scraper.utils import random_delay


from selenium.common.exceptions import TimeoutException

def search_jobs(driver, job_title, location):
    print("🔍 Opening LinkedIn Jobs SEARCH (forced)")

    job_title = job_title.replace(" ", "%20")
    location = location.replace(" ", "%20")

    search_url = (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={job_title}"
        f"&location={location}"
        "&f_TPR=r604800"   # last 7 days
        "&sortBy=R"
    )

    driver.get(search_url)
    time.sleep(8)

    # 🔥 FORCE CLICK INTO SEARCH RESULTS
    driver.execute_script("""
        const btn = document.querySelector('a[href*="/jobs/search"]');
        if (btn) btn.click();
    """)
    time.sleep(5)


def extract_job_cards(driver, max_pages=3):
    jobs = set()  # use set to avoid duplicates

    print("📄 Starting job link extraction")

    for page in range(max_pages):
        print(f"📃 Page {page + 1}")
        time.sleep(4)

        links = driver.find_elements(
            By.XPATH,
            "//a[contains(@href, '/jobs/view/')]"
        )

        print(f"🔎 Found {len(links)} job links")

        for link in links:
            url = link.get_attribute("href")
            if url and "/jobs/view/" in url:
                jobs.add(url.split("?")[0])

        # scroll whole page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

    job_list = list(jobs)
    print("🧪 DEBUG: total job links collected =", len(job_list))
    return job_list
