'''
**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) using a 74HC595 shift register (sr1). The goal is to display specific characters on the 7-segment display in a timed sequence.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should be off.
Display Sequence: The 7-segment display should follow a sequence of displays, each lasting 2 seconds:
First 2 Seconds: Display the character '0'.
Next 2 Seconds: Display the character 'A'.
Final 2 Seconds: Display the character 'P'.
This sequence should repeat continuously after the final display.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock

def test(driver, clock, args, deviation=0.2):
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    status = np.array([*sevseg1_value])
    correct = 0
    cur_time = get_clock(clock.text)
    char_lst = ['0','A','P']
    correct = char_lst[(int(cur_time)//2)%3]
    correct = np.array([*sevseg_value[correct[0]]])
    is_correct = np.allclose(status, correct, atol=deviation)
    return is_correct
        


def test_func(driver, clock, args, res):
    # test 1: 1s
    time.sleep(1)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 2: 3s
    time.sleep(2)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 3: 5s
    time.sleep(2)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    
    return res