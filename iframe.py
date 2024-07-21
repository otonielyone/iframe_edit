from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import urllib.request
import time
import csv
import re
import sys
import os, shutil



def setup_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    return driver


def login(driver, timeout, add_username, add_password):
    #Go to page - will redirect to login
    driver.get("https://www.websiteeditor.realtor/home/site/94fbcdbc/rentals")

    #Find username
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//input[@name="j_username"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    add_email = driver.find_element(by=By.XPATH, value='//input[@name="j_username"]')
    add_email.send_keys(add_username)
    

    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//input[@name="j_password"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    add_pass = driver.find_element(by=By.XPATH, value='//input[@name="j_password"]')
    add_pass.send_keys(add_password)


    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//button[text()="Login"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    login = driver.find_element(by=By.XPATH, value='//button[text()="Login"]')
    login.click()

def duplicate_row(driver, timeout, mls):
    try:
        element_present = EC.presence_of_element_located((By.ID, '_preview'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
            print("Timed out waiting for Login Page to Load")
            sys.exit()

    iframe = driver.find_element(by=By.ID, value="_preview")
                                
    # Switch to the iframe
    driver.switch_to.frame(iframe)

    find = driver.find_element(by=By.XPATH, value='//body[@id="dmRoot"]//div[@data-title="Text & Image"]')

    # Scroll to the element inside the iframe using JavaScript
    driver.execute_script("arguments[0].scrollIntoView(true);", find)

    find.click()

def main():
    timeout = 20
    add_username = "otonielyone@gmail.com"
    add_password = "Exotica12345"
    driver = setup_options()
    login(driver, timeout, add_username, add_password)

    list = ["VAFX2192025"]
    for mls in list:
        duplicate_row(driver,timeout, mls)

        
    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()
