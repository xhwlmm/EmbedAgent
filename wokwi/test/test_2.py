'''
**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) using a push button (k1).

**Detail Rules**:
Initialization: Upon powering on or resetting, the RGB LED should be off.
Button Interaction: Each press of the button (k1) should cycle the RGB LED through a sequence of colors:
First Press: LED displays red.
Second Press: LED displays green.
Third Press: LED displays blue.
Fourth Press: LED turns off.
This sequence should repeat with each subsequent press of the button.
'''
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import numpy as np
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, click_button

def test(driver, btn_cnt, args, deviation=0.2):
    rgb1_value = get_rgb_value(args['rgb1'], driver)
    status = np.array([*rgb1_value])
    if btn_cnt % 4 == 0:
        target = np.array([0, 0, 0])
    elif btn_cnt % 4 == 1:
        target = np.array([1, 0, 0])
    elif btn_cnt % 4 == 2:
        target = np.array([0, 1, 0])
    elif btn_cnt % 4 == 3:
        target = np.array([0, 0, 1])
    return np.allclose(status, target, atol=deviation)


        


def test_func(driver, clock, args, res): 
    actions = ActionChains(driver)
    # test 1: 
    btn_cnt = 0
    time.sleep(1)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)

    # test 2: click the button 1 times
    btn_cnt += 1
    click_button(args['k1'], actions)
    time.sleep(1)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)

    # test 3: click the button 2 times
    btn_cnt += 1
    click_button(args['k1'], actions)
    time.sleep(1)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)

    # test 4: click the button 2 times
    btn_cnt += 1
    click_button(args['k1'], actions)
    time.sleep(1)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)
    

    return res