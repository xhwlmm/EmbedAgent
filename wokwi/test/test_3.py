'''
**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (led1) using three push buttons (k1, k2, k3). The RGB LED should cycle through red, green, and blue colors upon startup, and the buttons should allow the user to control the LED's behavior.

**Detail Rules**:
Initialization: Upon powering on or resetting, the RGB LED (led1) should start cycling through red, green, and blue colors, with each color displayed for 2 seconds.

Button Interaction:
1. Pressing btn1 (k1) should stop the color cycling and keep the LED displaying the current color.
2. Pressing btn2 (k2) should resume the color cycling from the point it was stopped.
3. Pressing btn3 (k3) should turn off the RGB LED (led1), making it completely dark.

State Transitions:
- **Cycling Mode**: The LED cycles through red, green, and blue, each for 2 seconds.
- **Hold Mode**: The LED stops cycling and remains on the last color displayed before btn1 was pressed.
- **Off Mode**: The LED turns off completely.

The system should respond to button presses immediately and transition between these states as described.
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

def test_func(driver, clock, args, res):  
    actions = ActionChains(driver)
    # test 1: circle mode, red, green, blue
    time.sleep(1)
    rgb1_value = get_rgb_value(args['led1'], driver)
    time.sleep(1.5)
    rgb2_value = get_rgb_value(args['led1'], driver)
    time.sleep(2)
    rgb3_value = get_rgb_value(args['led1'], driver)
    if np.allclose(np.array([*rgb1_value, *rgb2_value, *rgb3_value]), np.array([1, 0, 0, 0, 1, 0, 0, 0, 1]),0.2):
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 2: stop circle mode
    click_button(args['k3'], actions)
    time.sleep(1)
    rgb1_value = get_rgb_value(args['led1'], driver)
    if np.allclose(np.array(rgb1_value), np.array([0, 0, 0]),0.2):
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 3: resume circle mode
    click_button(args['k2'], actions)
    time.sleep(2)
    rgb1_value = get_rgb_value(args['led1'], driver)
    time.sleep(2)
    rgb2_value = get_rgb_value(args['led1'], driver)
    time.sleep(2)
    rgb3_value = get_rgb_value(args['led1'], driver)
    if np.allclose(np.array([*rgb1_value, *rgb2_value, *rgb3_value]), np.array([1, 0, 0, 0, 1, 0, 0, 0, 1]),0.2) or np.allclose(np.array([*rgb3_value, *rgb1_value, *rgb2_value]), np.array([1, 0, 0, 0, 1, 0, 0, 0, 1]),0.2) or np.allclose(np.array([*rgb2_value, *rgb3_value, *rgb1_value]), np.array([1, 0, 0, 0, 1, 0, 0, 0, 1]),0.2):
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 4: stop circle mode
    click_button(args['k1'], actions)
    time.sleep(2)
    rgb1_value = get_rgb_value(args['led1'], driver)
    time.sleep(2)
    rgb2_value = get_rgb_value(args['led1'], driver)
    if np.allclose(np.array([*rgb1_value]), np.array([*rgb2_value]),0.2):
        res['msg'].append(1)
    else:
        res['msg'].append(0)


    return res