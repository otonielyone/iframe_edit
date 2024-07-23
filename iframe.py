import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    driver.execute_script('arguments[0].click();', login)
    driver.execute_script('arguments[0].click();', login)


def enter_iframe(driver, timeout, mls):
    try:
        element_present = EC.presence_of_element_located((By.ID, '_preview'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
            print("Timed out waiting for Login Page to Load")
            sys.exit()

    iframe = driver.find_element(by=By.ID, value="_preview")
    driver.switch_to.frame(iframe)
    

def duplicate_row(driver, timeout, mls):
    #Find element and scroll to it
    find = driver.find_element(by=By.XPATH, value='//body[@id="dmRoot"]//div[@data-title="Text & Image"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", find)
  
    #Get the elements HTML and replicate the div
    original_element_html = find.get_attribute('outerHTML')
    duplicate_element_html = f"<div>{original_element_html}</div>"
    driver.execute_script("arguments[0].insertAdjacentHTML('afterend', arguments[1]);", find, duplicate_element_html)
    
    #Select the newly created div
    new_element = find.find_element(By.XPATH, './following-sibling::div')
    
    #Find CSS version of the new elelemnt and click it to reveal menu
    div_element = new_element.find_element(By.CSS_SELECTOR, "div.wrapper")
    driver.execute_script('arguments[0].click();', div_element)

    # Switch back to default content
    driver.switch_to.default_content()

    try:
        element_present = EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'street:')]"))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
            print("Timed out waiting for Login Page to Load")
            sys.exit()

    #Find line 1/5 street
    y = driver.find_element(by=By.XPATH, value="//span[contains(text(),'street:')]")
    if y:
        driver.execute_script("arguments[0].scrollIntoView(true);", y)
        street = "street: 10804 Violet Ct"
        driver.execute_script("arguments[0].innerText = arguments[1];", y, street)

    #Find line 2/5 unit
    o = driver.find_element(by=By.XPATH, value="//span[contains(text(),'unit:')]")
    if o:
        driver.execute_script("arguments[0].scrollIntoView(true);", o)
        unit = "apt/unit: None"
        driver.execute_script("arguments[0].innerText = arguments[1];", o, unit)

    #Find line 3/5 county
    n = driver.find_element(by=By.XPATH, value="//span[contains(text(),'county:')]")
    if n:
        driver.execute_script("arguments[0].scrollIntoView(true);", n)
        county = "county: Manassas"
        driver.execute_script("arguments[0].innerText = arguments[1];", n, county)

    #Find line 4/5 zip
    e = driver.find_element(by=By.XPATH, value="//span[contains(text(),'zip:')]")
    if e:
        driver.execute_script("arguments[0].scrollIntoView(true);", e)
        zip = "zip: 20109"
        driver.execute_script("arguments[0].innerText = arguments[1];", e, zip)

    #Find line 5/5 cost
    r = driver.find_element(by=By.XPATH, value="//span[contains(text(),'cost:')]")
    if r:
        driver.execute_script("arguments[0].scrollIntoView(true);", r)
        cost = "cost: $2000"
        driver.execute_script("arguments[0].innerText = arguments[1];", r, cost)


def change_alt_text(driver, timeout, mls):

    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'input.textBox--input.TextBox-layout-full-22_m_9ua.TextBox-main-Ap_m_9ua.TextBox-valid-1d_m_9ua[aria-label="Alt text"]'))
        WebDriverWait(driver, timeout).until(element_present)

    except TimeoutException:
            print("Timed out waiting for Login Page to Load")
            sys.exit()

    #Find line 5/5 cost
    alt_txt = driver.find_element(by=By.CSS_SELECTOR, value='input.textBox--input.TextBox-layout-full-22_m_9ua.TextBox-main-Ap_m_9ua.TextBox-valid-1d_m_9ua[aria-label="Alt text"]')
    if alt_txt:
        print('found')
        # Define the value you want to set
        txt = "Listing: $2000 10804 Violet Ct, Manassas VA 20109"

        # Clear the existing text (if any) and set the new value
        alt_txt.clear()  # Clear existing text
        alt_txt.send_keys(txt)  # Set new value

def change_popup(driver, timeout, mls):
    ##click popup section
    section = WebDriverWait(driver, timeout).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'label.Label-module-main-26_m_9ua.Label-module-noOverflow-Fd_m_9ua.Label-module-noWhiteSpaceWrap-25_m_9ua.Label-module-hideOnEmpty-2H_m_9ua.Label-module-fixLastPadding-2Y_m_9ua[data-auto="label"]'))
    )
    popup_section = driver.find_element(by=By.CSS_SELECTOR, value='label.Label-module-main-26_m_9ua.Label-module-noOverflow-Fd_m_9ua.Label-module-noWhiteSpaceWrap-25_m_9ua.Label-module-hideOnEmpty-2H_m_9ua.Label-module-fixLastPadding-2Y_m_9ua[data-auto="label"]')
    driver.execute_script('arguments[0].click();', popup_section)
    #Click pop up and revel inner menu

    inner = "//div[contains(text(),'Popup')]"
    # Wait for the section to be clickable
    section = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, inner))
    )
    section.click()
 
   #Select drop down menu
    xpath_section = '//section[contains(@class, "DropdownField-main-2a_m_9ua")]'
    # Wait for the section to be clickable
    section = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath_section))
    )
    section.click()
    #Select entry
    xpath_dropdown_value = f'//input[@role="combobox"]'
    try_me = driver.find_elements(by=By.XPATH, value=xpath_dropdown_value)
    driver.execute_script('arguments[0].click();', try_me[2])
    try_me[2].send_keys(f'{mls[0]}')
    try_me[2].send_keys(Keys.ENTER)

def change_photo(driver, timeout, mls):
    css_section = "img[alt='text_image_widget_default_image.jpg']"
    # Wait for the section to be clickable
    section = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_section))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", section)
    section.click()

    d = f'//div[@data-auto="uploadImages"]//div[@role="button"]'
    # Wait for the section to be clickable
    section = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, d))
    )
    if section: 
        print('found upload')
        #section.click()

def select_photo(driver, timeout, mls):
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')  # Adjust XPath as needed
        
        # Provide the full path to the file you want to upload
        file_path = f'/home/oyone/Downloads/{mls[0]}.jpg'  # Adjust based on your actual file path
        
        # Upload the file using send_keys
        file_input.send_keys(file_path)

def main():
    timeout = 20
    add_username = "otonielyone@gmail.com"
    add_password = "Exotica12345"
    driver = setup_options()
    login(driver, timeout, add_username, add_password)

    list = [["VAR1234567", "1232 Clay Ave #1A, Bronx NY 10456"]]
    for mls in list:
        enter_iframe(driver, timeout, mls)
        duplicate_row(driver,timeout, mls[0])
        change_alt_text(driver, timeout, mls)
        change_popup(driver, timeout, mls)
        change_photo(driver, timeout, mls)
        select_photo(driver, timeout, mls)

    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()
