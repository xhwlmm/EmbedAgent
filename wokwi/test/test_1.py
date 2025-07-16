'''
**Task**:
You are tasked with programming an Arduino (uno) to control two LEDs (led1 and led2) in a specific sequence.

**Detail Rules**:
Initialization: Upon powering on or resetting, both LEDs (led1 and led2) should be off.
Sequence of Operation:
1. After 5 seconds, LED1 (led1) should turn on.
2. After another 5 seconds (total of 10 seconds from start), LED2 (led2) should turn on.
3. After another 5 seconds (total of 15 seconds from start), both LEDs (led1 and led2) should turn off simultaneously.
4. The sequence should then repeat after a 5-second delay.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock

def test(driver, clock, args, deviation=0.2):
    led1_value = get_led_value(args['led1'], driver)
    led2_value = get_led_value(args['led2'], driver)
    if get_clock(clock.text) < 5:
        return led1_value < 0.5 and led2_value < 0.5
    elif get_clock(clock.text) < 10:
        return led1_value > 0.5 and led2_value < 0.5
    elif get_clock(clock.text) < 15:
        return led1_value > 0.5 and led2_value > 0.5
    else:
        return led1_value < 0.5 and led2_value < 0.5

        


def test_func(driver, clock, args, res):    
    # test 1: in 1s, dark, dark
    time.sleep(1)
    res["msg"].append(1 if test(driver, clock, args) else 0)

    # test 2: in 6s, light, dark
    time.sleep(5)
    res["msg"].append(1 if test(driver, clock, args) else 0)

    # test 3: in 11s, light, light
    time.sleep(5)
    res["msg"].append(1 if test(driver, clock, args) else 0)

    # test 3: in 16s, dark, dark
    time.sleep(5)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    

    return res
