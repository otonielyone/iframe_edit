import json
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

    find = driver.find_element(by=By.XPATH, value='//body[@id="dmRoot"]//div[@data-title="Text & Image"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", find)
  
    original_element_html = find.get_attribute('outerHTML')
    duplicate_element_html = f"<div>{original_element_html}</div>"
    driver.execute_script("arguments[0].insertAdjacentHTML('afterend', arguments[1]);", find, duplicate_element_html)
    
    new_element = find.find_element(By.XPATH, './following-sibling::div')

    
    # Switch back to default content
    div_element = new_element.find_element(By.CSS_SELECTOR, "div.wrapper")
    driver.execute_script('arguments[0].click();', div_element)

    driver.switch_to.default_content()

    # Wait for element outside iframe to appear
 #   element_present = WebDriverWait(driver, 10).until(
 #       EC.visibility_of_element_located((By.ID, "widgetEditorWrapper"))
 #   )

    # Check if element is found
#    if element_present:
#            print('found')                
#    
#            if div_element:    
#                f = driver.find_elements(by=By.CSS_SELECTOR, value='div.groupContainer')
#                print("Found and visible.")
#
    y = driver.find_element(by=By.XPATH, value="//span[contains(text(),'Here will Go the address')]")
    if y:
        driver.execute_script("arguments[0].scrollIntoView(true);", y)
     #y.send_keys('test')

                ## Get the current text content
                #current_text = f[5].text
                #print("Current text:", current_text)

                ## Replace the text content with a new value
        new_text = "New text value"
        driver.execute_script("arguments[0].innerText = arguments[1];", y, new_text)
#spacing        
                #if div_element:    
                #    f = driver.find_elements(by=By.CSS_SELECTOR, value='div.groupContainer.Container-main-11_m_t63._group.Group-module-main-eV_m_t63.Group-module-flex-1o_m_t63')
                #    driver.execute_script("arguments[0].scrollIntoView(true);", f[3])
                #    f[3].click()
                #    print("Found and visible.")



        # Handle the next_div as needed
def main():
    timeout = 20
    add_username = "otonielyone@gmail.com"
    add_password = "Exotica12345"
    driver = setup_options()
    login(driver, timeout, add_username, add_password)

    list = [["VAFX2192025", "1232 Clay Ave #1A, Bronx NY 10456"]]
    for mls in list:
        enter_iframe(driver, timeout, mls)
        duplicate_row(driver,timeout, mls[0])
        #Swap out text in new element
        #Add main photo
        #Add in pop up 

            
    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    main()
