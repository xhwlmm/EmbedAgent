'''

**Task**:
You are tasked with programming an Arduino (uno) to control three RGB LEDs (rgb1, rgb2, rgb3) and three servos (servo1, servo2, servo3). The RGB LEDs will cycle through a sequence of colors, and the servos will move to specific angles in sync with the color changes. The system should create a synchronized light and motion display.

**Detail Rules**:
Initialization: Upon powering on or resetting, all RGB LEDs should be off, and all servos should be at their 0-degree position.
Color and Servo Sequence:
1. The RGB LEDs (rgb1, rgb2, rgb3) will cycle through the following colors in sequence: red, green, blue, yellow, cyan, magenta, and white.
2. Each color should be displayed for 2 seconds.
3. When the color changes, the servos (servo1, servo2, servo3) should move to specific angles corresponding to the current color:
   - Red: Servo1 at 0°, Servo2 at 45°, Servo3 at 90°.
   - Green: Servo1 at 45°, Servo2 at 90°, Servo3 at 135°.
   - Blue: Servo1 at 90°, Servo2 at 135°, Servo3 at 180°.
   - Yellow: Servo1 at 135°, Servo2 at 180°, Servo3 at 0°.
   - Cyan: Servo1 at 180°, Servo2 at 0°, Servo3 at 45°.
   - Magenta: Servo1 at 0°, Servo2 at 45°, Servo3 at 90°.
   - White: Servo1 at 90°, Servo2 at 135°, Servo3 at 180°.
4. After completing the sequence, the system should repeat the cycle indefinitely.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,get_sevseg_value,correct_sleep
from untils import sevseg_value

def test(clock, driver, args, deviation=0.2):
   colors = [
       [1, 0, 0],
       [0, 1, 0],
       [0, 0, 1],
       [1, 1, 0],
       [0, 1, 1],
       [1, 0, 1],
       [1, 1, 1]
   ]
   servo_digrees = [
       [0, 45, 90],
       [45, 90, 135],
       [90, 135, 180],
       [135, 180, 0],
       [180, 0, 45],
       [0, 45, 90],
       [90, 135, 180]
   ]
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   servo3_value = get_servo_value(args['servo3'],driver)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   rgb3_value = get_rgb_value(args['rgb3'], driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_index = (cur_time // 2) % 7
   correct_answer = [*colors[correct_index],*colors[correct_index],*colors[correct_index], *servo_digrees[correct_index]]
   current_answer = [*rgb1_value, *rgb2_value, *rgb3_value, servo1_value, servo2_value, servo3_value]
   return np.allclose(correct_answer, current_answer, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(8.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res