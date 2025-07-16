'''

**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1), a 7-segment display (sevseg1), and a servo motor (servo1) using a shift register (sr1). The RGB LED will cycle through a sequence of colors, the 7-segment display will show a countdown from 9 to 0, and the servo motor will rotate to a specific angle based on the countdown value. The system should repeat this sequence indefinitely.

**Detail Rules**:
Initialization: Upon powering on or resetting, the RGB LED (rgb1) should be off, the 7-segment display (sevseg1) should show "9", and the servo motor (servo1) should be at 0 degrees.
Sequence Execution:
1. The RGB LED (rgb1) will cycle through the following colors in sequence: Red, Green, Blue, Yellow, Cyan, Magenta, White. Each color should be displayed for 2 seconds.
2. Simultaneously, the 7-segment display (sevseg1) will count down from 9 to 0, with each number displayed for 2 seconds.
3. The servo motor (servo1) will rotate to an angle corresponding to the current countdown value (e.g., 0 degrees for 9, 20 degrees for 8, ..., 180 degrees for 0).
4. After reaching 0, the system should reset and repeat the sequence.
All hardware states should be updated synchronously.

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
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   servo1_value = get_servo_value(args['servo1'],driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_index = (cur_time // 2) % 7
   correct_num = 9 - (cur_time // 2) % 10
   correct_answer = [*colors[correct_index], *sevseg_value[str(correct_num)]]
   current_answer = [*rgb1_value, *sevseg1_value]
   return np.allclose(correct_answer, current_answer, atol=deviation) and abs(servo1_value - (180 - correct_num*20)) < 1

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(0.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(2.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(4.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(6.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res