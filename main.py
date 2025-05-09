from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Wait until the search input element is visible
try:
    search_input = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input.jobs-search-box__text-input.jobs-search-box__keyboard-text-input.jobs-search-box__ghost-text-input"))
    )
    print("Search input is visible!")
    
    # Now you can interact with the search bar (e.g., send keys)
    search_input.send_keys("Data Engineer")
except TimeoutException:
    print("Search input not found within the time limit.")
    # You can also take a screenshot to help debug:
    driver.save_screenshot("error_screenshot.png")