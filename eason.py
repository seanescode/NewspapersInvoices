import glob
import os
import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from constants import driver


def log_in_and_download_invoices(number_of_stores, account_number, password, downloads_folder):
    for i in range(number_of_stores):
        driver.find_element(By.ID, 'Username').send_keys(account_number[i])
        driver.find_element(By.ID, 'Password').send_keys(password[i])
        driver.find_element(By.CSS_SELECTOR, "button[class='button button--orange login-button']").click()
        try:
            WebDriverWait(driver, 7).until(ec.element_to_be_clickable((By.XPATH, '/html/body/nav/div/ul/li[6]/a'))).click()
        except TimeoutException:
            print("TimeoutException: perhaps incorrect username or password was inputted. Will continue to next store")
            driver.find_element(By.ID, 'Username').clear()  # reset the value of Username to empty if log in fails
            driver.find_element(By.ID, 'Password').clear()  # reset the value of Password to empty if log in fails

        WebDriverWait(driver, 7).until(ec.element_to_be_clickable((By.ID, 'download-note'))).click()  # download btn
        download_again_if_size_zero_bytes(downloads_folder)  # sometimes eason doesn't download right due to glitch
        WebDriverWait(driver, 7).until(ec.element_to_be_clickable((By.XPATH, '/html/body/header/div[1]/div/div[2]/span[2]/a'))).click()


#  try download again if it doesn't download properly (sometimes on Eason site it downloads but file is 0 Bytes)
def download_again_if_size_zero_bytes(downloads_folder):
    #  wait until pdf download shows up in downloads folder
    count_items_in_downloads = len(glob.glob(downloads_folder + r"\*"))
    items_in_downloads_after_download = count_items_in_downloads + 1
    while count_items_in_downloads < items_in_downloads_after_download:
        time.sleep(0.1)
        count_items_in_downloads = len(glob.glob(downloads_folder + r"\*"))

    #  check does file exist first - even if is in downloads folder it may be a temporary crdownload
    #  file (which would throw file not found error)
    does_file_exist = False
    while not does_file_exist:
        try:
            # can break out of while once latest file has the .pdf extension
            if os.path.splitext(max(glob.glob(downloads_folder + r"\*"), key=os.path.getctime))[1] == ".pdf":
                does_file_exist = True
        except FileNotFoundError:
            time.sleep(0.1)

    #  try to download again if downloaded with size not greater than 0 Bytes
    while not os.path.getsize(max(glob.glob(downloads_folder + r"\*"), key=os.path.getctime)) > 0:
        os.remove(max(glob.glob(downloads_folder + r"\*"), key=os.path.getctime))
        WebDriverWait(driver, 7).until(ec.element_to_be_clickable((By.ID, 'download-note'))).click()  # download btn
