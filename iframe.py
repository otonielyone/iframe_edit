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
    
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@name="j_username"]')))
    add_email = driver.find_element(By.XPATH, '//input[@name="j_username"]')
    add_email.send_keys(add_username)
    
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@name="j_password"]')))
    add_pass = driver.find_element(By.XPATH, '//input[@name="j_password"]')
    add_pass.send_keys(add_password)
    
    await asyncio.sleep(3)  # Adjust as needed
    
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-auto="login-button"]')))
    login_button = driver.find_element(By.XPATH, '//button[@data-auto="login-button"]')
    driver.execute_script('arguments[0].click();', login_button)
    
async def enter_iframe(driver, timeout):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, '_preview')))
    except TimeoutException:
        print("Timed out waiting for Iframe to Load")
        sys.exit()

    iframe = driver.find_element(By.ID, '_preview')
    driver.switch_to.frame(iframe)

async def widget_section(driver, timeout, mls):
    #click widget section
    txt = "(//label[normalize-space()='Widgets'])[1]" 
    widget_section = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, txt)))
    widget_section.click()


async def design_tab(driver, timeout, mls):
    try:
        design = "//span[normalize-space()='Design']"
        section = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, design)))
        section.click()
    except Exception as e:
        print(f"Error se;ecting design tab: {e}")

async def add_button(driver, timeout, mls):
    ntxt = "//span[@data-component-name='Typography' and text()='Button']"
    widget = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, ntxt)))
    driver.execute_script("arguments[0].scrollIntoView(true);", widget)
    widget.click()

async def add_btn_txt(driver, timeout, mls):
    button_txt ="//input[@placeholder='New Button']"
    address = mls[1]
    cost = "$2000"
    desc = f'{cost} - {address}'
    
    btn_txt_field = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, button_txt)))
    btn_txt_field.clear()
    btn_txt_field.send_keys(desc)
    btn_txt_field.send_keys(Keys.ENTER)
    await asyncio.sleep(1)

async def change_popup(driver, timeout, mls):
    try:
        inner = "//div[contains(text(),'Popup')]"
        section = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, inner)))
        section.click()

        xpath_dropdown_value = f'//input[@role="combobox"]'
        try_me = driver.find_elements(By.XPATH, xpath_dropdown_value)
        driver.execute_script('arguments[0].click();', try_me[3])
        try_me[3].send_keys(f'{mls[0]}')
        try_me[3].send_keys(Keys.ENTER)
        await asyncio.sleep(1)

    except Exception as e:
        print(f"Error changing popup: {e}")

async def change_btn_width(driver, timeout, mls):
    try:
        px_xpath = "//input[@value='222px']"
        px_txt_box = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, px_xpath)))
        px_txt_box.click()
        px_txt_box.clear()
        px_txt_box.send_keys("500px")
        px_txt_box.send_keys(Keys.ENTER)
        await asyncio.sleep(1)

    except Exception as e:
        print(f"Error selecting design tab: {e}")

async def change_btn_border(driver, timeout, mls):
    try:
        border = "//input[@value='1px']"
        txt_box = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, border)))
        txt_box.click()
        txt_box.clear()
        txt_box.send_keys(Keys.ENTER)
        await asyncio.sleep(1)

    except Exception as e:
        print(f"Error selecting design tab: {e}")

async def close_element_menu(driver, timeout):
    close_txt = "span[data-auto='close-widget-editor'] svg" 
   
    # Wait for the span element to be visible
    span_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, close_txt))
    )
    span_element.click()

async def move_button(driver, timeout, mls):
    # Find the iframe element
    iframe = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@id='_preview']"))
    )
    driver.switch_to.frame(iframe)

    xpath_expression = f"//span[contains(text(), '{mls[1]}')]"
    span_element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath_expression))
    )
    
    variable_value3 = "Click here download the Rental Representation Agreement"
    xpath_expression3 = f"//span[contains(text(), '{variable_value3}')]"
    span_element3 = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath_expression3))
    )
    action = ActionChains(driver)
    action.click_and_hold(span_element)

    try:
        driver.execute_script("arguments[0].scrollIntoView();", span_element3)
        action.move_to_element(span_element3).perform()
    except:
        driver.execute_script("arguments[0].scrollIntoView();", span_element3)
        action.move_to_element(span_element3).perform()
    try:
        action.move_to_element(span_element3).perform()
    except:
        driver.execute_script("arguments[0].scrollIntoView();", span_element3)
        action.move_to_element(span_element3).perform()

    action.release().perform()
    driver.execute_script("arguments[0].scrollIntoView();", span_element)


    

async def publish(driver, timeout):
    xpath_expression = f"//span[normalize-space()='Republish']"
    republish = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath_expression))
    )
    republish.click()
    await asyncio.sleep(timeout)

async def main():
    timeout = 20
    add_username = "otonielyone@gmail.com"
    add_password = "Exotica12345"
    driver = await setup_driver()

    await login(driver, timeout, add_username, add_password)
    mls_list = ("VAR1234567", "1232 Clay Ave #1A, Bronx NY 10456","$2000"), ("VAR7654321", "2321 Yalc Ave #1B, Bronx NY 65501", "$0002"), ("VAR1234567", "1232 Clay Ave #1A, Bronx NY 10456","$2000"), ("VAR7654321", "2321 Yalc Ave #1B, Bronx NY 65501", "$0002")
        
    for mls in mls_list:
        await widget_section(driver, timeout, mls)
        await add_button(driver, timeout, mls)
        await add_btn_txt(driver, timeout, mls)
        await change_popup(driver, timeout, mls)
        await design_tab(driver, timeout, mls)
        await change_btn_width(driver, timeout, mls)
        await change_btn_border(driver, timeout, mls)
        await close_element_menu(driver, timeout)
        await move_button(driver, timeout, mls)
        driver.switch_to.default_content()

    await publish(driver, timeout)    
    await asyncio.sleep(timeout)

if __name__ == "__main__":
    asyncio.run(main())
