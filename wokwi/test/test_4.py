'''
**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) so that it blinks in different colors according to a specific sequence.

**Detail Rules**:
Initialization: Upon powering on or resetting, the RGB LED should be off.
Color Sequence: The RGB LED should follow a sequence of colors, each lasting for 3 seconds:
First 3 Seconds: The LED should display red.
Next 3 Seconds: The LED should display yellow (a combination of red and green).
Following 3 Seconds: The LED should display white (a combination of red, green, and blue).
Final 3 Seconds: The LED should turn off.
This sequence should repeat indefinitely after the final step.
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
    cur_time = int(get_clock(clock.text))//3
    rgb1_value = get_rgb_value(args['rgb1'], driver)
    status = np.array([*rgb1_value])
    if cur_time % 4 == 0:
        target = np.array([1, 0, 0])
    elif cur_time % 4 == 1:
        target = np.array([1, 1, 0])
    elif cur_time % 4 == 2:
        target = np.array([1, 1, 1])
    elif cur_time % 4 == 3:
        target = np.array([0, 0, 0])
    return np.allclose(status, target, atol=deviation)
        


def test_func(driver, clock, args, res):    
    # test 1: in 1s, red
    time.sleep(1)
    res["msg"].append(1 if test(driver, clock, args) else 0)

    # test 2: in 4s, yellow
    time.sleep(3)
    res["msg"].append(1 if test(driver, clock, args) else 0)

    # test 3: in 7s, white
    time.sleep(3)
    res["msg"].append(1 if test(driver, clock, args) else 0)

    # test 4: in 10s, null
    time.sleep(3)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    

    return res