import asyncio
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

async def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    return driver

async def login(driver, timeout, add_username, add_password):
    driver.get("https://www.websiteeditor.realtor/home/site/94fbcdbc/rentals")
    
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@name="j_username"]')))
    except TimeoutException:
        print("Timed out waiting for Login Page to Load")
        sys.exit()

    add_email = driver.find_element(By.XPATH, '//input[@name="j_username"]')
    add_email.send_keys(add_username)

    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@name="j_password"]')))
    except TimeoutException:
        print("Timed out waiting for Password Field")
        sys.exit()

    add_pass = driver.find_element(By.XPATH, '//input[@name="j_password"]')
    add_pass.send_keys(add_password)

    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Login"]')))
    except TimeoutException:
        print("Timed out waiting for Login Button")
        sys.exit()

    login = driver.find_element(By.XPATH, '//button[text()="Login"]')
    driver.execute_script('arguments[0].click();', login)

async def enter_iframe(driver, timeout, mls):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, '_preview')))
    except TimeoutException:
        print("Timed out waiting for Iframe to Load")
        sys.exit()

    iframe = driver.find_element(By.ID, '_preview')
    driver.switch_to.frame(iframe)

async def duplicate_row(driver, timeout, mls):
    try:
        find = driver.find_element(By.XPATH, '//body[@id="dmRoot"]//div[@data-title="Text & Image"]')
        driver.execute_script("arguments[0].scrollIntoView(true);", find)
        original_element_html = find.get_attribute('outerHTML')
        duplicate_element_html = f"<div>{original_element_html}</div>"
        driver.execute_script("arguments[0].insertAdjacentHTML('afterend', arguments[1]);", find, duplicate_element_html)
        new_element = find.find_element(By.XPATH, './following-sibling::div')
        div_element = new_element.find_element(By.CSS_SELECTOR, "div.wrapper")
        driver.execute_script('arguments[0].click();', div_element)
    except Exception as e:
        print(f"Error duplicating row: {e}")

async def description(driver, timeout, mls):
    try:
        await asyncio.sleep(1)  # A small delay to ensure the iframe is fully loaded
        driver.switch_to.default_content()

        y = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'street:')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", y)
        street = "street: 10804 Violet Ct"
        driver.execute_script("arguments[0].innerText = arguments[1];", y, street)

        o = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'unit:')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", o)
        unit = "apt/unit: None"
        driver.execute_script("arguments[0].innerText = arguments[1];", o, unit)

        n = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'county:')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", n)
        county = "county: Manassas"
        driver.execute_script("arguments[0].innerText = arguments[1];", n, county)

        e = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'zip:')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", e)
        zip_code = "zip: 20109"
        driver.execute_script("arguments[0].innerText = arguments[1];", e, zip_code)

        r = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'cost:')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", r)
        cost = "cost: $2000"
        driver.execute_script("arguments[0].innerText = arguments[1];", r, cost)

        driver.switch_to.default_content()  # Switch back to default content after interacting with iframe
    except Exception as e:
        print(f"Error setting description: {e}")

async def change_alt_text(driver, timeout, mls):
    try:
        alt_txt = driver.find_element(By.XPATH, "//input[@aria-label='Alt text']")
        txt = "Listing: $2000 10804 Violet Ct, Manassas VA 20109"
        alt_txt.clear()
        alt_txt.send_keys(txt)
    except Exception as e:
        print(f"Error changing alt text: {e}")

async def change_popup(driver, timeout, mls):
    try:
        section = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='fa fa-chevron-right']")))
        driver.execute_script('arguments[0].click();', section)

        inner = "//div[contains(text(),'Popup')]"
        section = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, inner)))
        section.click()

        xpath_section = "//span[@id='react-select-4--value']//div[@class='Select-value']"
        section = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath_section)))
        section.click()

        xpath_dropdown_value = f'//input[@role="combobox"]'
        try_me = driver.find_elements(By.XPATH, xpath_dropdown_value)
        driver.execute_script('arguments[0].click();', try_me[2])
        try_me[2].send_keys(f'{mls[0]}')
        try_me[2].send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Error changing popup: {e}")

async def change_photo(driver, timeout, mls):
    try:
        css_section = "//button[normalize-space()='Replace']"
        section = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, css_section)))
        driver.execute_script("arguments[0].scrollIntoView(true);", section)
        section.click()

        file_input_xpath = '//input[@type="file"]'
        file_input = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, file_input_xpath)))

        file_path = f'/home/oyone/Downloads/{mls[0]}.jpg'
        file_input.send_keys(file_path)

        await enter_iframe(driver, timeout, mls)

        add_me = "div[id='1210442206"
        u = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, add_me)))
        driver.execute_script('arguments[0].click();', u)
    except Exception as e:
        print(f"Error changing photo: {e}")

async def main():
    timeout = 20
    add_username = "otonielyone@gmail.com"
    add_password = "Exotica12345"
    driver = await setup_driver()

    try:
        await login(driver, timeout, add_username, add_password)
        mls_list = [["VAR1234567", "1232 Clay Ave #1A, Bronx NY 10456"]]
        for mls in mls_list:
            await enter_iframe(driver, timeout, mls)
            await duplicate_row(driver, timeout, mls[0])
            await description(driver, timeout, mls)
            await change_alt_text(driver, timeout, mls)
            await change_popup(driver, timeout, mls)
            await change_photo(driver, timeout, mls)

    finally:
        await asyncio.sleep(10)
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
