'''

**Task**:
You are tasked with programming an Arduino (uno) to control a servo motor (servo1). The servo motor should sweep its position back and forth between 0° and 180° in increments of 10°, with each position held for 2 seconds before moving to the next.

**Detail Rules**:
Initialization: Upon powering on or resetting, the servo motor (servo1) should start at the 0° position.
Sweep Operation:
1. The servo motor should move from 0° to 180° in increments of 10°, holding each position for 2 seconds.
2. After reaching 180°, the servo motor should reverse direction and move back to 0° in decrements of 10°, again holding each position for 2 seconds.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,correct_sleep

def test(clock, driver, args):
    servo1_value = get_servo_value(args['servo1'],driver)
    cur_time = get_clock(clock.text)
    cnt = cur_time//2
    correct_rotate = 10*cnt % 360
    if correct_rotate > 180:
        correct_rotate = 360 - correct_rotate
    return abs(correct_rotate - servo1_value) < 1
        


def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.3, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(4.3, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(6.3, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    

    return res
