'''

**Task**:
You are tasked with programming an Arduino (uno) to control two servo motors (servo1, servo2) using two push buttons (btn1, btn2) and two slide potentiometers (pot1, pot2). The servo motors should rotate to specific angles based on the values of the potentiometers when the corresponding buttons are pressed. Each button controls one servo motor, and the potentiometers determine the target angle for the respective servo.

**Detail Rules**:
Initialization: Upon powering on or resetting, both servo motors (servo1, servo2) should be set to their initial position (0 degrees).
Button and Potentiometer Interaction:
1. When the first button (btn1) is pressed, the first servo motor (servo1) should rotate to an angle determined by the value of the first potentiometer (pot1). The potentiometer value should be mapped to a range of 0 to 180 degrees.
2. When the second button (btn2) is pressed, the second servo motor (servo2) should rotate to an angle determined by the value of the second potentiometer (pot2). The potentiometer value should also be mapped to a range of 0 to 180 degrees.
3. The servo motors should maintain their positions until the corresponding button is pressed again with a new potentiometer value.
4. Each button press should be debounced to avoid false triggers caused by mechanical vibrations.

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

def test(correct_answer, args, driver, deviation=1):
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    return np.allclose([servo1_value, servo2_value], correct_answer, atol=deviation)

        


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    click_button(args['btn1'], actions)
    move_pot(args['pot1'], 1, driver)
    correct_answer = [0,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(correct_answer, args, driver) else 0)
    # test 2: click the button
    click_button(args['btn1'], actions)
    correct_answer = [180,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(correct_answer, args, driver) else 0)

    # test 3: click the button twice
    move_pot(args['pot2'], 1, driver)
    click_button(args['btn2'], actions)
    correct_answer = [180,180]
    time.sleep(0.5)
    res["msg"].append(1 if test(correct_answer, args, driver) else 0)

    # test 4: click the button three times
    move_pot(args['pot1'], 0, driver)
    click_button(args['btn1'], actions)
    correct_answer = [0,180]
    time.sleep(0.5)
    res["msg"].append(1 if test(correct_answer, args, driver) else 0)
    
    return res