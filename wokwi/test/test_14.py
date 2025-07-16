'''
**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) using a 74HC595 shift register (sr1). The goal is to create a timer that increments by 2 seconds every real-time second, and once the timer exceeds 10 seconds, only the last digit of the timer should be displayed on the 7-segment display.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should be off.
Timer Operation: Every real-time second, the timer should increment by 2 seconds. The 7-segment display should update to show the current timer value.
Display Rule: If the timer value exceeds 10 seconds, only the last digit of the timer value should be displayed on the 7-segment display. For example, if the timer is at 12 seconds, the display should show '2'.
The timer should continue to increment and update the display accordingly, following the above rules.
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
    status = np.array([*sevseg1_value])
    correct = 0
    cur_time = get_clock(clock.text)
    correct = str(int(cur_time)*2%10)
    correct = np.array([*sevseg_value[correct[0]]])
    is_correct = np.allclose(status, correct, atol=deviation)
    return is_correct
        


def test_func(driver, clock, args, res):
    # test 1: 1s
    correct_sleep(1.1,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 2: 3s
    correct_sleep(3.1,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 3: 6s
    correct_sleep(6.1,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    
    return res