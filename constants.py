import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

df = pd.read_excel('Template News & Mags.xlsx', sheet_name='Passwords')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.set_window_position(-10000, 0)  # hide browser so running automation script in background

