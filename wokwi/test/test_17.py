'''
**Task**:
You are tasked with programming an Arduino (uno) to control a red LED (led1), a blue LED (led2), and an RGB LED (rgb1). The goal is to create a sequence where the red LED and the RGB LED display red, followed by the blue LED and the RGB LED displaying blue, in a continuous loop.

**Detail Rules**:
Initialization: Upon powering on or resetting, the red LED (led1) should be on, the blue LED (led2) should be off, and the RGB LED (rgb1) should display red.
Sequence:
1. First State: The red LED (led1) is on, the blue LED (led2) is off, and the RGB LED (rgb1) displays red. This state should last for 2 seconds.
2. Second State: The red LED (led1) turns off, the blue LED (led2) turns on, and the RGB LED (rgb1) displays blue. This state should also last for 2 seconds.
The sequence should repeat indefinitely, alternating between the two states every 2 seconds.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock,correct_sleep

def test(driver, clock, args, deviation=0.2):
    rgb1_value = get_rgb_value(args['rgb1'], driver)
    led1_value = get_led_value(args['led1'], driver)
    led2_value = get_led_value(args['led2'], driver)
    status = np.array([*rgb1_value, led1_value, led2_value])
    cur_time = get_clock(clock.text)
    if (cur_time // 2) % 2 == 0:
        correct = np.array([1, 0, 0, 1, 0])
        is_correct = np.allclose(status, correct, atol=deviation)
        return is_correct
    else:
        correct = np.array([0, 0, 1, 0, 1])
        is_correct = np.allclose(status, correct, atol=deviation)
        return is_correct
        


def test_func(driver, clock, args, res):    
    # test 1: in 1s, red, red, null
    correct_sleep(0.5,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)

    # test 2: in 3s, null, blue, blue
    correct_sleep(2.5,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)

    # test 3: in 5s, red, red, null
    correct_sleep(4.5,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    

    return res