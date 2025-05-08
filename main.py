from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

time.sleep(15)