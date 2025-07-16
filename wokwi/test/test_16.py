'''
**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2) and a push button (btn1). The 7-segment displays will show a two-digit number, where one display represents the tens digit and the other represents the units digit. The push button will increment the displayed number by 37 each time it is pressed. If the number exceeds 99, it should reset to 0.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00".
Button Interaction: Each press of the button (btn1) should increment the displayed number by 37. The number should be displayed on the two 7-segment displays, with the tens digit on one display (sevseg1) and the units digit on the other (sevseg2).
Reset Condition: If the number exceeds 99 after incrementing, both displays should reset to "00".
Display Update: The 7-segment displays should immediately update to reflect the new number after each button press.
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
    sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
    status = np.array([*sevseg1_value, *sevseg2_value])
    correct = 0
    for i in range(btn_cnt):
        correct += 37
        if correct > 99:
            correct = 0
    correct = str(correct).zfill(2)
    correct = np.array([*sevseg_value[correct[0]], *sevseg_value[correct[1]]])
    is_correct = np.allclose(status, correct, atol=deviation)
    return is_correct
        


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_cnt = 0
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)
    # test 2: click the button
    btn_cnt+=1
    click_button(args['btn1'], actions)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)

    # test 3: click the button twice
    btn_cnt+=1
    click_button(args['btn1'], actions)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)

    # test 4: click the button three times
    btn_cnt+=1
    click_button(args['btn1'], actions)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)
    
    return res