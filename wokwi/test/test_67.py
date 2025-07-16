'''

**Task**:
You are tasked with programming an Arduino (uno) to control two servo motors (servo1, servo2) using a push button (btn1). The servos should alternate their positions between 0° and 180° each time the button is pressed. Specifically, when the button is pressed, servo1 should move to 180° and servo2 should move to 0°, and vice versa on the next press.

**Detail Rules**:
Initialization: Upon powering on or resetting, both servos (servo1, servo2) should be set to 0°.
Button Interaction: Each press of the button (btn1) should toggle the positions of the servos. If servo1 is at 0° and servo2 is at 180°, pressing the button should move servo1 to 180° and servo2 to 0°. The next press should reverse their positions again.
Debouncing: The button press should be debounced to avoid false triggers caused by mechanical vibrations.
Servo Movement: The servos should move smoothly to their new positions after each button press.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,sevseg_value,get_sevseg_value,click_button,get_servo_value

def test(btn_cnt, args, driver, deviation=1):
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    btn_cnt = btn_cnt % 2
    current = [servo1_value,servo2_value]
    if btn_cnt == 0:
        return np.allclose(current, [0,180], atol=deviation)
    elif btn_cnt == 1:
        return np.allclose(current, [180,0], atol=deviation)
        


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_cnt = 0
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, args, driver) else 0)
    # test 2: click the button
    btn_cnt+=1
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, args, driver) else 0)

    # test 3: click the button twice
    btn_cnt+=1
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, args, driver) else 0)
    
    return res