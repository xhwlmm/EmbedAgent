from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from untils import wait_for_element, random_wait, copy_text, read_json, paste_text, print_body,get_hardwares,complete_connection
from untils import WOKWI_USER_ID,WOKWI_TEST_ID,platform_parts,some_xpath
import argparse
from tqdm import tqdm
import time
import json
import re
import os

def extract_code(response,mark,lang=""):
    response = response.split("</think>")[-1]
    response = response.replace("[\\/","[/")
    response = response.replace("[ /","[/")
    mark_end = mark.replace("[", "[/")
    raw_response = response
    flag = False
    if response.find(mark) != -1:
        response = response.split(mark)[1]
        if response.find(mark_end) != -1:
            response = response.split(mark_end)[0]
        flag = True
    if lang != "" and response.find("```" + lang) != -1:
        # use re extrat ```lang ```
        try:
            response = re.findall(r'```' + lang + r'(.+?)```', response, re.DOTALL)[-1]
        except:
            response += "```"
            response = re.findall(r'```' + lang + r'(.+?)```', response, re.DOTALL)[-1]
        flag = True
    if flag == False:
        return False
    return response
    
def process_predict(correct, predict, task, platform):
    processed_res = {}
    # with_connection
    if task == "with_connection":
        for i in range(len(correct)):
            diagram = correct[i]["diagram"][platform]
            new_diagram = str(diagram).replace("'",'"')
            sketch = extract_code(predict[i]["response"],"[Arduino Code]","arduino")
            processed_res[i] = {"diagram": new_diagram, "sketch": sketch}
        return processed_res
    elif task == "without_connection":
        for i in range(len(correct)):
            diagram = correct[i]["diagram"][platform]
            connection = extract_code(predict[i]["response"],"[CONNECTIONS]","connections")
            if type(diagram) == str:
                hardwares = get_hardwares(eval(diagram))
            else:
                hardwares = get_hardwares(diagram)
            new_diagram = complete_connection(connection, hardwares, platform)
            sketch = extract_code(predict[i]["response"],"[Arduino Code]","cpp")
            if new_diagram == False:
                processed_res[i] = {"diagram": False, "sketch": sketch}
            else:
                new_diagram = str(new_diagram).replace("'",'"')
                processed_res[i] = {"diagram": new_diagram, "sketch": sketch}
        return processed_res
    elif task.startswith("translate"):
        _,platform,lang = task.split('_')
        if "python" in task:
            for i in range(len(correct)):
                diagram = correct[i]["diagram"]['Arduino Mega']
                connection = extract_code(predict[i]["response"],"[CONNECTIONS]")
                if type(diagram) == str:
                    hardwares = get_hardwares(eval(diagram))
                else:
                    hardwares = get_hardwares(diagram)
                new_diagram = complete_connection(connection, hardwares, platform)
                sketch = extract_code(predict[i]["response"],f"[{platform} Code]","python")
                if new_diagram == False:
                    processed_res[i] = {"diagram": False, "main.py": sketch}
                else:
                    new_diagram = str(new_diagram).replace("'",'"')
                    processed_res[i] = {"diagram": new_diagram, "main.py": sketch}
            return processed_res
        if "ESP-IDF" in task:
            for i in range(len(correct)):
                diagram = correct[i]["diagram"]['Arduino Mega']
                connection = extract_code(predict[i]["response"],"[CONNECTIONS]")
                if type(diagram) == str:
                    hardwares = get_hardwares(eval(diagram))
                else:
                    hardwares = get_hardwares(diagram)
                new_diagram = complete_connection(connection, hardwares, platform)
                sketch = extract_code(predict[i]["response"],f"[{platform} Code]","c")
                if new_diagram == False:
                    processed_res[i] = {"diagram": False, "main.c": sketch}
                else:
                    new_diagram = str(new_diagram).replace("'",'"')
                    processed_res[i] = {"diagram": new_diagram, "main.c": sketch}
            return processed_res
    else:
        for i in range(len(predict)):
            diagram = str(predict[i]["diagram"]).replace("'",'"')
            sketch = extract_code(predict[i]["response"],"[Arduino Code]","cpp")
            processed_res[i] = {"diagram": diagram, "sketch": sketch}
        return processed_res
    # TODO other task
        
def update_project(WOKWI_USER_ID, url, data, error_time):
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
    time.sleep(1 + error_time*2)
    try:
        error_button = driver.find_element(By.XPATH, some_xpath['error_button'])
        error_button.click()
    except:
        pass
    if 'sketch' in data: 
        # get sketch.ino
        sketch_button = driver.find_element(By.XPATH, "//button[text()='sketch.ino']")
        sketch_button.click()
        random_wait()
        paste_text(driver, some_xpath['current_file'], data["sketch"])
    elif 'main.py' in data:
        # get main.py
        main_button = driver.find_element(By.XPATH, "//button[text()='main.py']")
        main_button.click()
        random_wait()
        paste_text(driver, some_xpath['current_file'], data["main.py"])
    elif 'main.c' in data:
        # get main.c
        main_button = driver.find_element(By.XPATH, "//button[text()='main.c']")
        main_button.click()
        random_wait()
        paste_text(driver, some_xpath['current_file'], data["main.c"])
    # get diagram.json
    diagram_button = driver.find_element(By.XPATH, "//button[text()='diagram.json']")
    diagram_button.click()
    random_wait()
    paste_text(driver, some_xpath['current_file'], data["diagram"])
    # save
    # save_button = wait_for_element(some_xpath['save_button'],'xpath',driver)
    # driver.save_screenshot('screenshot.png')
    # save_button.click()

    random_wait()
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_path', type=str, default='./dataset/test_url.json')
    parser.add_argument('--task', type=str, default='without_connection', help='with_connection, without_connection, translate_platform_lang')
    parser.add_argument('--data_path', type=str, default='./dataset/prompt.jsonl')
    parser.add_argument('--lang', type=str, default='c')
    parser.add_argument('--total_data', type=int, default=81)
    parser.add_argument('--model_name', type=str, default='')
    parser.add_argument('--platform', type=str, default='Arduino Mega')
    parser.add_argument('--user_id', type=str, default=WOKWI_TEST_ID)
    parser.add_argument('--root_path', type=str, default='../dataset/infer_results')
    args = parser.parse_args()
    
    # read url
    url_dict = read_json(args.url_path)
    # upload
    correct = read_json(args.data_path)
    correct = correct[:args.total_data:]
    correct_status = ['success_upload', 'connection_error', 'format_error']
    predict = read_json(f"{args.root_path}/{args.model_name}/{args.task}.json")
    output_path = f"{args.root_path}/{args.model_name}/{args.task}_compile.jsonl"

    if not os.path.exists(output_path):
        data = [i for i in range(args.total_data)]
    else:
        data = []
        status = read_json(output_path)
        for item in status:
            if item['status'] not in correct_status:
                data.append(item['id'])
    
    processed_predict = process_predict(correct, predict, args.task, args.platform)
    with open(output_path, 'w', encoding='utf-8') as f:
        for index in tqdm(range(args.total_data)):
            title = f"{index}_{args.lang}"
            url = url_dict[title]
            hardware_data = processed_predict[index]
            if index not in data:
                f.write(json.dumps(status[index], ensure_ascii=False) + '\n')
                continue
            if hardware_data["diagram"] == False:
                f.write(json.dumps({"id":index, "status": "connection_error"}, ensure_ascii=False) + '\n')
                continue
            if hardware_data.get('sketch',True) == False or hardware_data.get('main.py',True) == False or hardware_data.get('main.c',True) == False:
                f.write(json.dumps({"id":index, "status": "format_error"}, ensure_ascii=False) + '\n')
                continue
            for i in range(3):
                try:
                    update_project(args.user_id, url, hardware_data, i)
                    random_wait()
                    f.write(json.dumps({"id":index, "status": "success_upload"}, ensure_ascii=False) + '\n')
                    print({"id":index, "status": "success_upload"})
                    break
                except Exception as e:
                    print(i,e)
                    if i == 2:
                        print(f"upload {title} failed")
                        f.write(json.dumps({"id":index, "status": "upload_error"}, ensure_ascii=False) + '\n')
                        continue
                    time.sleep(5*(i+1))
