
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from untils import wait_for_element, random_wait, copy_text
from untils import WOKWI_TEST_ID,WOKWI_USER_ID
import json
import argparse
import time

def get_url(WOKWI_USER_ID, output_file, url="https://wokwi.com/dashboard/projects"):
    # init
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    random_wait()
    driver.execute_script(f"window.localStorage.setItem('wokwiUser', '{WOKWI_USER_ID}');window.location.reload();")
    wait_for_element("/html/body/div/div/ul", 'xpath', driver)

    url_dic = {}
    # scroll down to the bottom
    previous_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_wait()
        random_wait()

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == previous_height:
            break
        previous_height = new_height

    # get all projects
    projects = driver.find_elements(By.XPATH, "/html/body/div/div/ul/*")
    for project in projects:
        href = project.find_element(By.CLASS_NAME, "project-list-tile_projectName__TN5xl")
        url_dic[href.text] = href.get_attribute("href")
    try:
        url_dic = dict(sorted(url_dic.items(), key=lambda x: int(x[0])))
    except:
        url_dic = url_dic
    with open(f"{output_file}","w",encoding='utf-8') as f:
        json.dump(url_dic, f, ensure_ascii=False, indent=4)

    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_path', type=str, default='../dataset/test_url.json')
    parser.add_argument('--user_id', type=str, default=WOKWI_TEST_ID)
    args = parser.parse_args()
    get_url(args.user_id, args.url_path)