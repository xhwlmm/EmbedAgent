'''

Task:
You are tasked with programming an Arduino (uno) to control a servo motor (servo1) using three slide potentiometers (pot1, pot2, pot3). The servo motor's position will be determined by the combined input from the three potentiometers. Each potentiometer will control a specific aspect of the servo's behavior: one for the minimum angle, one for the maximum angle, and one for the current position.

Detail Rules:
Initialization: Upon powering on or resetting, the servo motor (servo1) should be set to its default position (0 degrees).
Potentiometer Interaction:
1. The first potentiometer (pot1) determines the minimum angle of the servo motor. The value of pot1 is mapped to a range of 0 to 90 degrees.
2. The second potentiometer (pot2) determines the maximum angle of the servo motor. The value of pot2 is mapped to a range of 90 to 180 degrees.
3. The third potentiometer (pot3) controls the current position of the servo motor. The value of pot3 is mapped to the range defined by the minimum (pot1) and maximum (pot2) angles.
4. The servo motor's position should be updated continuously based on the current values of the potentiometers.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value

def test_func(driver, clock, args, res):
    # test 1
    move_pot(args['pot2'],1,driver)
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    if abs(servo1_value-0) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 2
    move_pot(args['pot3'],1,driver)
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    if abs(servo1_value-180) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 3
    move_pot(args['pot2'],0,driver)
    move_pot(args['pot3'],1,driver)
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    if abs(servo1_value-90) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    return res