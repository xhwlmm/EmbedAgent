'''
**Task**:
You are tasked with programming an Arduino (uno) to control the brightness of a single-color LED (led1) using three slide potentiometers (pot1, pot2, pot3). The potentiometers will determine the upper and lower bounds of the LED's brightness, as well as the actual brightness level.

**Detail Rules**:
Initialization: Upon powering on or resetting, the LED (led1) should be off.
Potentiometer Interaction:
1. The first potentiometer (pot1) determines the upper bound of the LED's brightness. The value of pot1 is mapped uniformly from 0 to 1.
2. The second potentiometer (pot2) determines the lower bound of the LED's brightness. The value of pot2 is also mapped uniformly from 0 to 1.
3. The third potentiometer (pot3) controls the actual brightness of the LED. The value of pot3 is mapped uniformly from the lower bound (pot2) to the upper bound (pot1).
4. If the upper bound (pot1) is greater than or equal to the lower bound (pot2), the LED's brightness should be set according to the mapped value of pot3.
5. If the upper bound (pot1) is less than the lower bound (pot2), the LED should remain off.
The LED's brightness should be updated continuously based on the current values of the potentiometers.
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
    # test 1: move pot1 0, pot2 0, pot3 1
    move_pot(args['pot1'],0,driver)
    move_pot(args['pot2'],0,driver)
    move_pot(args['pot3'],1,driver)
    time.sleep(1)
    led_value = get_led_value(args['led1'], driver)
    if abs(led_value-0) < 0.2:
        res["msg"].append(1)
    else:
        res["msg"].append(0)
    

    # test 2: move pot1 1, pot2 1, pot3 0
    move_pot(args['pot1'],1,driver)
    move_pot(args['pot2'],1,driver)
    move_pot(args['pot3'],0,driver)
    time.sleep(1)
    led_value = get_led_value(args['led1'], driver)
    if abs(led_value-1) < 0.2:
        res["msg"].append(1)
    else:
        res["msg"].append(0)

    # test 3: move pot1 0, pot2 1, pot3 1
    move_pot(args['pot1'],0,driver)
    move_pot(args['pot2'],1,driver)
    move_pot(args['pot3'],1,driver)
    time.sleep(1)
    led_value = get_led_value(args['led1'], driver)
    if abs(led_value-0) < 0.2:
        res["msg"].append(1)
    else:
        res["msg"].append(0)
    # test 4: move pot1 1, pot2 0, pot3 0
    move_pot(args['pot1'],1,driver)
    move_pot(args['pot2'],0,driver)
    move_pot(args['pot3'],0,driver)
    time.sleep(1)
    led_value = get_led_value(args['led1'], driver)
    if abs(led_value-0) < 0.2:
        res["msg"].append(1)
    else:
        res["msg"].append(0)
    # test 5: move pot1 1, pot2 0, pot3 1
    move_pot(args['pot1'],1,driver)
    move_pot(args['pot2'],0,driver)
    move_pot(args['pot3'],1,driver)
    time.sleep(1)
    led_value = get_led_value(args['led1'], driver)
    if abs(led_value-1) < 0.2:
        res["msg"].append(1)
    else:
        res["msg"].append(0)

    return res