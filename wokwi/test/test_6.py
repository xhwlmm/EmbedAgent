'''
**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) using a slide potentiometer (pot1). The goal is to adjust the color of the RGB LED based on the position of the slide potentiometer.

**Detail Rules**:
Initialization: Upon powering on or resetting, the RGB LED should be off.
Slide Potentiometer Interaction: The position of the slide potentiometer (pot1) should determine the color of the RGB LED (rgb1) as follows:
- When the potentiometer is in the first third of its range, the LED should display red.
- When the potentiometer is in the second third of its range, the LED should display green.
- When the potentiometer is in the final third of its range, the LED should display blue.
The LED should continuously update its color based on the current position of the potentiometer.
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

def test(driver, pot_pos, args, deviation=0.2):
    rgb1_value = get_rgb_value(args['rgb1'], driver)
    status = np.array([*rgb1_value])
    if pot_pos < 0.33:
        target = np.array([1,0,0])
    elif pot_pos < 0.66:
        target = np.array([0,1,0])
    else:
        target = np.array([0,0,1])
    return np.allclose(status, target, atol=deviation)


        


def test_func(driver, clock, args, res): 
    actions = ActionChains(driver)
    # test 1: move the pot to 0
    move_pot(args['pot1'],0,driver)
    time.sleep(1)
    res["msg"].append(1 if test(driver, 0, args) else 0)

    # test 2: move the pot to 0.5
    move_pot(args['pot1'],1,driver)
    time.sleep(1)
    res["msg"].append(1 if test(driver, 1, args) else 0)

    # test 3: move the pot to 0.5
    move_pot(args['pot1'],0,driver)
    time.sleep(1)
    res["msg"].append(1 if test(driver, 0, args) else 0)

    return res