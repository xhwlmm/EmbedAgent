'''

**Task**:
You are tasked with programming an Arduino (uno) to control two RGB LEDs (rgb1, rgb2) and two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2). The RGB LEDs will cycle through a sequence of colors, and the 7-segment displays will show a two-digit number that increments every 2 seconds. The RGB LEDs and the 7-segment displays should operate independently but synchronously.

**Detail Rules**:
1. **RGB LEDs (rgb1, rgb2)**:
   - The RGB LEDs will cycle through the following sequence of colors: Red, Green, Blue, Yellow, Cyan, Magenta, White.
   - Each color should be displayed for 2 seconds before transitioning to the next color.
   - Both RGB LEDs should display the same color at the same time.

2. **7-Segment Displays (sevseg1, sevseg2)**:
   - The 7-segment displays will show a two-digit number starting from 00.
   - The number will increment by 1 every 2 seconds.
   - If the number exceeds 99, it should reset to 00.
   - One display (sevseg1) will show the tens digit, and the other display (sevseg2) will show the units digit.

3. **Shift Registers (sr1, sr2)**:
   - The shift registers will be used to control the 7-segment displays.
   - The Arduino will send data to the shift registers to update the displayed digits.

4. **Synchronization**:
   - The RGB LEDs and the 7-segment displays should operate independently but synchronously, meaning their timing should align (e.g., both update every 2 seconds).

5. **Initial State**:
   - On startup, the RGB LEDs should display Red, and the 7-segment displays should show "00".

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
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_index = (cur_time // 2) % 7
   correct_num = (cur_time // 2) % 100
   digit = correct_num % 10
   tens = correct_num // 10
   correct_answer = [*colors[correct_index],*colors[correct_index], *sevseg_value[str(tens)], *sevseg_value[str(digit)]]
   current_answer = [*rgb1_value, *rgb2_value, *sevseg1_value, *sevseg2_value]
   return np.allclose(correct_answer, current_answer, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(10.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(14.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res