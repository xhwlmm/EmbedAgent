
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from untils import wait_for_element, random_wait, copy_text, read_json, print_body
from untils import WOKWI_TEST_ID, WOKWI_USER_ID, some_xpath, TOT_DATA
import argparse
from tqdm import tqdm
import time
import json
def find_library(lib_name, driver):
    ul_element = wait_for_element(some_xpath['library_ul'],'xpath',driver)
    found = False
    pre_li_elements = []
    while not found:
        # driver.save_screenshot('screenshot.png')
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        if pre_li_elements == li_elements:
            break
        pre_li_elements = li_elements
        for li_element in li_elements:
            if li_element.text == lib_name:
                found = True
                return li_element
        if not found:
            driver.execute_script("arguments[0].scrollBy(0, 100)", ul_element)
            random_wait()
    return None
    
    
def add_library(lib_names, driver):
    library_file = wait_for_element("//button[text()='Library Manager']", 'xpath', driver)
    library_file.click()
    for lib_name in lib_names:
        add_library_button = wait_for_element(some_xpath['library_button'], 'xpath', driver)
        random_wait()
        add_library_button.click()
        input_library = wait_for_element(some_xpath['library_input'], 'xpath', driver)
        input_library.send_keys(lib_name)
        random_wait()
        time.sleep(2)
        library = find_library(lib_name, driver)
        if library is None:
            raise Exception(f"Library {lib_name} not found")
        library.click()
        random_wait()
        
    
    

def create_project(WOKWI_TEST_ID, url, title):
    # init
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    random_wait()
    driver.execute_script(f"window.localStorage.setItem('wokwiUser', '{WOKWI_TEST_ID}');window.location.reload();")
    if "arduino-uno" in url:
        add_library(['Servo'], driver)
    # click save button
    save_button = wait_for_element(some_xpath['save_button'],'xpath',driver)
    random_wait()
    if "arduino-uno" in url:
        save_button.click()
    else:
        # ctrl + s
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL).perform()
    random_wait()
    # driver.save_screenshot('screenshot.png')
    # add title
    wait_for_element(some_xpath['save_input'],'xpath',driver)
    driver.find_element(By.XPATH, some_xpath['save_input']).send_keys(title)
    # save
    save_button = wait_for_element(some_xpath['save_input_button'],'xpath',driver)
    save_button.click()
    random_wait()
    driver.quit()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', type=str, default='', help='with_connection, without_connection, translate_platform_lang')
    parser.add_argument('--lang', type=str, default='python', help='c,python,esp-idf')
    parser.add_argument('--user_id', type=str, default=WOKWI_TEST_ID)
    parser.add_argument('--num', type=int, default=TOT_DATA)
    args = parser.parse_args()
    
    # read url
    if args.lang == 'c':
        url = "https://wokwi.com/projects/new/arduino-uno"
    elif args.lang == 'python':
        url = "https://wokwi.com/projects/new/micropython-pi-pico"
    elif args.lang == 'esp-idf':
        url = "https://wokwi.com/projects/new/esp-idf-esp32"
    else:
        raise Exception(f"lang {args.lang} not supported")

    for project_id in tqdm(range(args.num)):
        title = f"{project_id}_{args.lang}"
        for i in range(3):
            try:
                create_project(WOKWI_TEST_ID, url, title)
                random_wait()
                break
            except Exception as e:
                print(i,e)
                if i == 2:
                    print(f"create {title} failed")
                    continue
                time.sleep(5*(i+1))