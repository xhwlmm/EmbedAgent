'''
**Task**:
You are tasked with programming an Arduino (uno) to control a single-color LED (led1) using a pushbutton (k1). The goal is to toggle the LED's state (on/off) each time the button is pressed.

**Detail Rules**:
Initialization: Upon powering on or resetting, the LED should be in the "on" state.
Button Interaction: Each press of the button (k1) should toggle the LED's state:
First Press: LED turns off.
Second Press: LED turns on.
Third Press: LED turns off.
Fourth Press: LED turns on.
This toggling sequence should continue with each subsequent press of the button. The LED should maintain its current state until the button is pressed again.
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
    led1_value = get_led_value(args['led1'], driver)
    status = np.array([led1_value])
    if btn_cnt % 2 == 0:
        target = np.array([1])
    elif btn_cnt % 2 == 1:
        target = np.array([0])
    return np.allclose(status, target, atol=deviation)


        


def test_func(driver, clock, args, res): 
    actions = ActionChains(driver)
    # test 1: init
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

    return res