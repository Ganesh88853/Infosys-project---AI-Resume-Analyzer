import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from backend.scraper.driver_manager import get_chrome_driver
from backend.scraper.linkedin_login import login_linkedin
from backend.scraper.job_search import open_job_search, extract_job_cards

driver = get_chrome_driver(headless=False)
login_linkedin(driver)
open_job_search(driver, "Data Analyst", "Bangalore")

input("Are jobs visible in browser? Press Enter.")
driver.quit()

cards = extract_job_cards(driver, max_pages=1)
print(len(cards))
print(cards[:2])
