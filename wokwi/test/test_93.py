'''

**Task**:
You are tasked with programming an Arduino (uno) to control two LEDs (led1, led2), a servo motor (servo1), and a slide potentiometer (pot1). The slide potentiometer will control the position of the servo motor, and the LEDs will indicate the direction of the servo's movement. When the servo moves clockwise, one LED (led1) will light up, and when it moves counterclockwise, the other LED (led2) will light up.

**Detail Rules**:
Initialization: Upon powering on or resetting, the servo motor (servo1) should be at 0 degrees, and both LEDs (led1, led2) should be off.
Potentiometer Interaction: The slide potentiometer (pot1) will control the servo's position. The potentiometer's value (0 to 1023) should be mapped to the servo's angle range (0 to 180 degrees).
LED Indication: 
1. If the servo is moving clockwise (angle increasing), LED (led1) should light up, and LED (led2) should remain off.
2. If the servo is moving counterclockwise (angle decreasing), LED (led2) should light up, and LED (led1) should remain off.
3. If the servo is stationary, both LEDs should remain off.
State Maintenance: Each state (clockwise, counterclockwise, or stationary) should be maintained for at least 2 seconds to allow for verification.

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


def test(clock, driver, args, preangle ,nowangle, deviation=0.2):
    led1_value = get_led_value(args['led1'],driver)
    led2_value = get_led_value(args['led2'],driver)
    servo1_value = get_servo_value(args["servo1"], driver)

    current = [led1_value, led2_value, servo1_value]
    if nowangle > preangle:
        correct = [1,0,180*nowangle]
    elif nowangle < preangle:
        correct = [0,1,180*nowangle]
    else:
        correct = [0,0,180*nowangle]

    return np.allclose(current, correct, deviation)

    
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    time.sleep(1)
    preangle = 0
    nowangle = 0
    res["msg"].append(1 if test(clock, driver, args, preangle, nowangle) else 0)

    # test 2
    time.sleep(2)
    preangle = 0
    nowangle = 1
    move_pot(args["pot1"],1,driver)
    time.sleep(1.5)
    res["msg"].append(1 if test(clock, driver, args, preangle, nowangle) else 0)

    # test 3
    time.sleep(2)
    preangle = 1
    nowangle = 0
    move_pot(args["pot1"],0,driver)
    time.sleep(1.5)
    res["msg"].append(1 if test(clock, driver, args, preangle, nowangle) else 0)

    return res