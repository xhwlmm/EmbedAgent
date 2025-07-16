'''
**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2). The goal is to create a timer that increments by 6 seconds for every real-world second that passes. Once the timer exceeds 99 seconds, it should only display the last two digits.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "0". The sevseg1 is in the extinguished state and sevseg2 show "0".
Timer Operation: Every real-world second, the timer should increment by 6 seconds. The updated time should be displayed on the 7-segment displays.
Display Rules: If the timer exceeds 99 seconds, only the last two digits of the timer should be displayed on the 7-segment displays. For example, if the timer reaches 102 seconds, the displays should show "2".
The timer should continue to increment and update the display every second, following the above rules.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,correct_sleep

def test(driver, clock, args, deviation=0.2):
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    cur_time = get_clock(clock.text)
    sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
    status = np.array([*sevseg1_value, *sevseg2_value])
    correct = 0
    correct = str(int(cur_time)*6%100).zfill(2)
    correct = np.array([*sevseg_value['null' if correct[0] == '0' else correct[0]], *sevseg_value[correct[1]]])
    is_correct = np.allclose(status, correct, atol=deviation)
    return is_correct
        


def test_func(driver, clock, args, res):
    # test 1: 1s
    correct_sleep(2.2,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 2: 3s
    correct_sleep(6.2,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 3: 6s
    correct_sleep(10.2,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    
    return res