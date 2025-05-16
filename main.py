from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import time

import os

# Chrome options
options = Options()
# options.add_argument("--headless") # Run without GUI

# Init webdriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())
                          ,options=options)

url = "https://www.linkedin.com/jobs/"
driver.get(url)

WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, 'session_key')))
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, 'session_password')))

username_field = driver.find_element(By.ID, "session_key")
password_field = driver.find_element(By.ID, "session_password")

# Replace with your LinkedIn username and password
username = os.getenv("LINKEDIN_USERNAME")
password = os.getenv("LINKEDIN_PASSWORD")

# Input credentials
username_field.send_keys(username)
password_field.send_keys(password)

# Find and click login button
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

# Wait for profile icon or "Jobs" tab
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/jobs/')]"))
)

driver.get("https://www.linkedin.com/jobs/")



location_search_input = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='address-level2']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", location_search_input)
location_search_input.click()
location_search_input.clear()
location_search_input.send_keys("Jakarta")

# Wait until the search input element is visible
job_role_search_input = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.jobs-search-global-typeahead__input"))
)
job_role_search_input.click()
job_role_search_input.clear()
job_role_search_input.send_keys("Data Engineer")

job_role_search_input.send_keys(Keys.RETURN)

date_posted_filter_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "searchFilter_timePostedRange"))
)
date_posted_filter_button.click()

label = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='timePostedRange-r86400']"))
)
label.click()

try:
    show_results_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH,"//button[starts-with(@aria-label, 'Apply current filter to show')]"))
    )
    show_results_button.click()
    print("✅ Clicked 'Show results'")

except Exception as e:
    driver.save_screenshot("debug_show_results_aria_error.png")
    print("❌ Failed to click 'Show results' button:", e)

time.sleep(7)