'''

**Task**:
Program the Arduino (uno) to control three servo motors (servo1, servo2, servo3) and a 10-segment LED bar graph (bargraph1). The servos will move in synchronized increments, and the LED bar graph will visually represent the combined position of all servos.

**Detail Rules**:
1. **Initialization**: All servos start at 0° position, and the LED bar graph (bargraph1) remains off.
2. **Servo Movement**:
   - Every 2 seconds, each servo increases its angle by 18° until reaching 180°, then decreases by 18° until reaching 0°, repeating indefinitely.
3. **LED Display**:
   - The total of all three servo angles (0-540) is divided into 10 equal ranges (54 units per LED).
   - The number of lit LEDs corresponds to the current total (e.g., total=162 lights 3 LEDs).
   - LED lights from pin A1 to A10.
4. **Synchronization**: All servos update their angles simultaneously every 2 seconds.

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
   servo1_value = get_servo_value(args["servo1"],driver)
   servo2_value = get_servo_value(args["servo2"],driver)
   servo3_value = get_servo_value(args["servo3"],driver)
   bargraph1_value = get_bargraph_value(args["bargraph1"], driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_num = cur_time // 2
   correct_servo_value = (correct_num * 18) % 360
   if correct_servo_value >= 180:
      correct_servo_value = 360-correct_servo_value
   correct_bargraph_value = correct_servo_value // 18
   correct_bargraph_value = [1 if i < correct_bargraph_value else 0 for i in range(10)]
   if abs(servo1_value - correct_servo_value) <= deviation and abs(servo2_value - correct_servo_value) <= deviation and abs(servo3_value - correct_servo_value) <= deviation and np.allclose(bargraph1_value,correct_bargraph_value,deviation):
      return True
   else:
      return False


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
    correct_sleep(12.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res