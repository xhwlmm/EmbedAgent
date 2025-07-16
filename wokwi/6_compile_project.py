from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from untils import wait_for_element, random_wait, copy_text, read_json, paste_text, print_body
from untils import WOKWI_USER_ID,WOKWI_TEST_ID,some_xpath
import argparse
from tqdm import tqdm
import time
import json
import re
import os
        
def compile_project(WOKWI_USER_ID, url):
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
    random_wait()
    try:
        time.sleep(2)
        random_wait()
        error = driver.find_element(By.ID, "form-dialog-title").text
        error_message = driver.find_element(By.XPATH, some_xpath['error_message']).text
        driver.quit()
        return {"status":error,"content":error_message}
    except:
        pass
    # compile
    compile_button = wait_for_element(some_xpath['compile_button'],'xpath',driver)
    compile_button.click()
    random_wait()
    element1_error = (By.ID, "form-dialog-title")
    element2_timeout = (By.XPATH, "xpath_for_element2")
    element3_success = (By.XPATH, some_xpath['stop_button'])
    element = WebDriverWait(driver, 30).until(
        EC.any_of(
            EC.presence_of_element_located(element1_error),
            EC.presence_of_element_located(element2_timeout),
            EC.presence_of_element_located(element3_success)
        )
    )
    if driver.find_elements(*element1_error):
        error = element.text
        error_message = driver.find_element(By.XPATH, some_xpath['error_message']).text
        driver.quit()
        return {"status":error,"content":error_message}
    elif driver.find_elements(*element3_success):
        driver.quit()
        return {"status":"sucess"}
    else:
        driver.quit()
        return {"status":"timeout"}
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_path', type=str, default='../dataset/test_url.json')
    parser.add_argument('--lang', type=str, default='c')
    parser.add_argument('--task', type=str, default='without_connection', help='with_connection, without_connection, translate_platform_lang')
    parser.add_argument('--root_path', type=str, default='../dataset/infer_results')
    parser.add_argument('--model_name', type=str, default='deepseek-coder-33b-instruct')
    parser.add_argument('--total_data', type=int, default=20)
    parser.add_argument('--user_id', type=str, default=WOKWI_TEST_ID)
    args = parser.parse_args()
    
    compile_file = f'{args.root_path}/{args.model_name}/{args.task}_compile.jsonl'
    if not os.path.exists(compile_file):
        raise FileNotFoundError(f'{compile_file} not found')
    else:
        data = []
        status = read_json(compile_file)
        for item in status:
            if item['status'] in ["timeout","runtime_error","success_upload"]:
                data.append(item['id'])
    

    # read url
    url_dict = read_json(args.url_path)
    # upload
    with open(compile_file,'w',encoding='utf-8') as f:
        for index in tqdm(range(args.total_data)):
            title = f"{index}_{args.lang}"
            url = url_dict[title]
            if index not in data:
                cur_res = status[index]
            else:
                try:
                    cur_res = compile_project(args.user_id, url)
                    cur_res['id'] = index
                    print(cur_res)
                except:
                    cur_res = {"status":"runtime_error", "id":index}
            f.write(json.dumps(cur_res,ensure_ascii=False)+'\n')
            random_wait()
