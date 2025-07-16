
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from untils import wait_for_element, random_wait, copy_text, read_json
from untils import WOKWI_USER_ID
import argparse
from tqdm import tqdm
import time
import json

def download_project(WOKWI_USER_ID, url,item):
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
    # get sketch.ino
    sketch = copy_text(driver, "/html/body/div[1]/div/main/div/div/div[1]/div[2]/div/div[2]/section/div/div/div[1]/div[2]/div[1]/div[4]")
    # get diagram.json
    diagram_button = driver.find_element(By.XPATH, "//button[text()='diagram.json']")
    diagram_button.click()
    random_wait()
    diagram = copy_text(driver, "/html/body/div[1]/div/main/div/div/div[1]/div[2]/div/div[2]/section/div/div/div[1]/div[2]/div[1]/div[4]")
    item["sketch"] = sketch
    item["diagram"] = diagram
    
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_path', type=str, default='../dataset/correct_url.json')
    parser.add_argument('--save_path', type=str, default='../dataset/correct.jsonl')
    args = parser.parse_args()
    
    # read url
    url_dict = read_json(args.url_path)
    # download
    with open(args.save_path, "w", encoding="utf-8") as f:
        for title, url in tqdm(url_dict.items()):
            for i in range(3):
                try:
                    print(i)
                    item = {"id": title, "url": url}
                    download_project(WOKWI_USER_ID, url, item)
                    random_wait()
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
                    break
                except Exception as e:
                    print(i,e)
                    if i == 2:
                        print(f"download {title} failed")
                        continue
                    time.sleep(5*(i+1))