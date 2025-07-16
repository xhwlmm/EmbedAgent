'''
**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) using a push button (btn1). The goal is to create a counter that increments by 3 each time the button is pressed, and the current count is displayed on the 7-segment display. The counter should reset to 0 after reaching 9.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should show 0.
Button Interaction: Each press of the button (btn1) should increment the counter by 3. The counter should wrap around to 0 after reaching 9. The updated count should be immediately displayed on the 7-segment display.
Debouncing: Ensure that the button press is debounced to avoid multiple increments from a single press.
Display Update: The 7-segment display should accurately reflect the current count after each button press.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,sevseg_value,get_sevseg_value,click_button

def test(driver, btn_cnt, args, deviation=0.2):
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    status = np.array([*sevseg1_value])
    correct = (btn_cnt * 3) % 10
    correct = str(correct)
    correct = np.array([*sevseg_value[correct[0]]])
    is_correct = np.allclose(status, correct, atol=deviation)
    return is_correct
        


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_cnt = 0
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)
    # test 2: click the button
    btn_cnt+=1
    click_button(args['btn1'],actions)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)

    # test 3: click the button twice
    btn_cnt+=1
    click_button(args['btn1'],actions)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)

    # test 4: click the button three times
    btn_cnt+=1
    click_button(args['btn1'],actions)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)
    
    return res