import os
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from backend.scraper.utils import random_delay

COOKIE_FILE = "linkedin_cookies.pkl"

def login_linkedin(driver):
    driver.get("https://www.linkedin.com/")
    time.sleep(3)

    # Load cookies if available
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "rb") as f:
            for cookie in pickle.load(f):
                cookie.pop("sameSite", None)
                driver.add_cookie(cookie)

        driver.get("https://www.linkedin.com/feed/")
        time.sleep(5)

        if "feed" in driver.current_url:
            print("✅ Logged in using cookies")
            return

    # Manual login
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)

    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    driver.find_element(By.ID, "username").send_keys(email)
    random_delay()
    driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)

    print("⚠️ Solve CAPTCHA if shown, then press Enter")
    input()

    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(driver.get_cookies(), f)

    print("✅ Logged in and cookies saved")
