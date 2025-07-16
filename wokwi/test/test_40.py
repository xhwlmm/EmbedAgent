'''

**Task**:
You are tasked with programming an Arduino (uno) to synchronize a 7-segment display (sevseg1) and a 10-LED bar graph (bargraph1) using a shift register (sr1). The system will cycle through values 0 to 9, where the 7-segment displays the numeric value and the bar graph visually represents the same value through illuminated LEDs.

**Detail Rules**:
1. **Initialization**:  
   - The 7-segment display (sevseg1) shows "0" and the bar graph (bargraph1) has no LEDs lit when the system starts.

2. **Automatic Cycling**:  
   - The displayed value increments by 1 every 2 seconds. After reaching 9, it resets to 0 and repeats indefinitely.

3. **Display Synchronization**:  
   - The 7-segment display (sevseg1) must show the current numeric value (0-9) using its segments.
   - The bar graph (bargraph1) must light up a number of LEDs equal to the current value. For example, if the value is 3, 3 LEDs are lit. (The order of LEDs is from pin:A1 to A10)

4. **Hardware Utilization**:  
   - The shift register (sr1) must drive the 7-segment display (sevseg1).  
   - The Arduino (uno) must directly control the bar graph (bargraph1) via its GPIO pins.

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
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   cur_index = (cur_time // 2) % 10
   correct = sevseg_value[str(cur_index)] + [1 if i < cur_index else 0 for i in range(10)]

   return np.allclose(sevseg1_value+bargraph1_value, correct, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(4.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(8.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(10.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res