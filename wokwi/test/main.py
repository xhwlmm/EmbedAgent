from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import argparse
import sys
import os
import time
import json
from tqdm import tqdm
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from untils import WOKWI_TEST_ID, WOKWI_USER_ID, some_xpath
from untils import read_json, print_body, random_wait,wait_for_element, copy_text

def eval_wokwi(WOKWI_USER_ID, url, test_func):
    # init
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    random_wait()
    # login
    # driver.execute_script(f"window.localStorage.setItem('wokwiUser', '{WOKWI_USER_ID}');window.location.reload();")
    start_button = wait_for_element(some_xpath['compile_button'],'xpath',driver)
    # get_args
    diagram_button = driver.find_element(By.XPATH, "//button[text()='diagram.json']")
    diagram_button.click()
    random_wait()
    diagram = copy_text(driver, some_xpath['current_file'])
    diagram = eval(diagram)
    args = {}
    for part in diagram['parts']:
        # TODO add more parts
        if part['id'] in ['uno']: continue
        args[part['id']] = driver.find_element(By.ID, part['id'])
        
    # start
    start_button.click()
    clock = wait_for_element('simulation_timeText__tR870', 'class', driver)
    # test
    res = {"status":"", "msg":[]}
    res = test_func(driver, clock, args, res)
    
    if res['msg'].count(0) == 0:
        res['status'] = 'pass'
    else:
        res['status'] = 'fail'
    driver.quit()
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_path', type=str, default='../../dataset/test_url.json')
    parser.add_argument('--total_data', type=int, default=20)
    parser.add_argument('--task', type=str, default='')
    parser.add_argument('--lang', type=str, default='c')
    parser.add_argument('--output_path', type=str, default='../../dataset/infer_results')
    parser.add_argument('--model_name', type=str, default='deepseek-coder-33b-instruct')
    parser.add_argument('--user_id', type=str, default=WOKWI_TEST_ID)
    parser.add_argument('--test_id', type=int, default=-1)
    args = parser.parse_args()
    urls_dic = read_json(args.url_path)

    if args.test_id != -1:
        i = args.test_id
        eval_module = __import__(f"test_{i}")
        test_func = eval_module.test_func
        url = urls_dic[f"{i}_c"]
        res = eval_wokwi(WOKWI_TEST_ID, url, test_func)
        random_wait()
        res['id'] = i
        res['url'] = url
        print(res)
    else:
        output_path = f"{args.output_path}/{args.model_name}/{args.task}_eval.jsonl"
        compile_path = f"{args.output_path}/{args.model_name}/{args.task}_compile.jsonl"
        compile_data = read_json(compile_path)
        with open(output_path, 'w' ,encoding='utf-8') as f:
            for i in tqdm(range(args.total_data)):
                title = f"{i}_{args.lang}"
                url = urls_dic[title]
                if compile_data is not None and compile_data[i]['status'] != 'sucess':
                    res = compile_data[i]
                else:
                    eval_module = __import__(f"test_{i}")
                    test_func = eval_module.test_func
                    for j in range(3):
                        try:
                            res = eval_wokwi(args.user_id, url, test_func)
                            random_wait()
                            break
                        except Exception as e:
                            time.sleep(5)
                            random_wait()
                            if j == 2:
                                res = {"status":"error", "msg": str(e) }
                            continue
                    res['id'] = i
                    res['url'] = url
                    print(res)
                    f.write(json.dumps(res, ensure_ascii=False) + '\n')

