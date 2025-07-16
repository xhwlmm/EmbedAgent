'''

**Task**:
You are tasked with programming an Arduino (uno) to control three RGB LEDs (rgb1, rgb2, rgb3), a 7-segment display (sevseg1), and three servo motors (servo1, servo2, servo3). The RGB LEDs will cycle through a sequence of colors, the 7-segment display will show a countdown from 9 to 0, and the servo motors will rotate to specific angles in sync with the countdown. The system should repeat this sequence indefinitely.

**Detail Rules**:
1. **RGB LEDs**:
   - The RGB LEDs (rgb1, rgb2, rgb3) will cycle through the following colors in sequence: Red, Green, Cyan, Magenta, Blue, Yellow, White.
   - Each color should be displayed for 2 seconds before transitioning to the next color.
   - All three RGB LEDs should display the same color simultaneously.

2. **7-Segment Display**:
   - The 7-segment display (sevseg1) will show a countdown from 9 to 0.
   - Each number should be displayed for 2 seconds before decrementing to the next number.
   - After reaching 0, the countdown should reset to 9 and repeat.

3. **Servo Motors**:
   - The servo motors (servo1, servo2, servo3) will rotate to specific angles in sync with the countdown:
     - When the countdown is 7-9, all servos should be at 0 degrees.
     - When the countdown is 4-6, all servos should be at 60 degrees.
     - When the countdown is 1-3, all servos should be at 120 degrees.
     - When the countdown is 0, all servos should be at 180 degrees.
   - The servos should hold their positions for 2 seconds before moving to the next angle.

4. **Synchronization**:
   - The RGB LEDs, 7-segment display, and servo motors should operate in sync, with each state lasting for 2 seconds.
   - The system should repeat the sequence indefinitely.

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
       [0, 1, 1],
       [1, 0, 1],
       [0, 0, 1],
       [1, 1, 0],
       [1, 1, 1]
   ]
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   rgb3_value = get_rgb_value(args['rgb3'], driver)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   servo1_value = get_servo_value(args['servo1'],driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_index = (cur_time // 2) % 7
   correct_num = 9 - (cur_time // 2) % 10
   correct_answer = [*colors[correct_index],*colors[correct_index],*colors[correct_index], *sevseg_value[str(correct_num)]]
   current_answer = [*rgb1_value,*rgb2_value,*rgb3_value, *sevseg1_value]
   return np.allclose(correct_answer, current_answer, atol=deviation) and abs(servo1_value - (((9-correct_num)//3)*60)) < 1

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(8.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(10.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res