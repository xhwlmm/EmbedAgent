'''

**Task**:
You are tasked with programming an Arduino (uno) to control two servos (servo1, servo2) and an RGB LED (rgb1) using three push buttons (btn1, btn2, btn3). The RGB LED will display different colors based on the state of the servos, and the push buttons will control the movement of the servos and the color of the RGB LED.

**Detail Rules**:
Initialization: Upon powering on or resetting, both servos (servo1, servo2) should be at their 0-degree position, and the RGB LED (rgb1) should be off.
Button Interaction:
1. The first button (btn1) will rotate servo1 (servo1) to 90 degrees and set the RGB LED (rgb1) to red.
2. The second button (btn2) will rotate servo2 (servo2) to 90 degrees and set the RGB LED (rgb1) to green.
3. The third button (btn3) will reset both servos (servo1, servo2) to their 0-degree position and set the RGB LED (rgb1) to blue.
Each state (servo position and LED color) should be maintained for at least 2 seconds to allow for verification.

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
from untils import sevseg_value,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,get_bargraph_value,click_button,get_servo_value



def test(clock, driver, args, btn_num, btn_ls, deviation = 0.2):
    servo1_value = get_servo_value(args["servo1"], driver)
    servo2_value = get_servo_value(args["servo2"], driver)

    rgb_value = get_rgb_value(args["rgb1"], driver)
    current = [servo1_value,servo2_value,*rgb_value]

    colors = [[0,0,0],
              [1,0,0],
              [0,1,0],
              [0,0,1]]

    if btn_num == 0:
        correct = [0,0] + colors[0]
    elif btn_num == 3:
        correct = [0,0] + colors[3]
    elif btn_num == 1:
        correct = [90*btn_ls[0],90*btn_ls[1]] + colors[1]
    else:
        correct = [90*btn_ls[0],90*btn_ls[1]] + colors[2]

    return np.allclose(current, correct, atol=deviation)


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init 
    time.sleep(1)
    bnt_num = 0
    btn_ls = [0,0,0]
    res["msg"].append(1 if test(clock, driver, args, bnt_num, btn_ls) else 0)

    # test 2: click the button1 
    bnt_num = 1
    btn_ls = [1,0,0]
    click_button(args['btn1'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, bnt_num, btn_ls) else 0)

    # test 3: click the button2 
    bnt_num = 2
    btn_ls = [1,1,0]
    click_button(args['btn2'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, bnt_num, btn_ls) else 0)

    # test 2: click the button3
    bnt_num = 3
    btn_ls = [1,1,1]
    click_button(args['btn3'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, bnt_num, btn_ls) else 0)

    return res