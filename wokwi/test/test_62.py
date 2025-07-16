'''

**Task**:
You are tasked with programming an Arduino (uno) to create a synchronized visual system using two RGB LEDs (rgb1, rgb2), two 7-segment displays (sevseg1, sevseg2), a 10-segment LED bar graph (bargraph1), and two shift registers (sr1, sr2). The system will display a number that increments automatically, with visual feedback distributed across multiple components.

**Detail Rules**:
Initialization: 
- Both 7-segment displays show "00"
- All bar graph LEDs are off
- RGB LEDs are off

Operation:
1. The displayed number increments by 1 every 2 seconds (0 → 1 → 2... → 99 → 00)
2. 7-segment displays (sevseg1, sevseg2) always show the current number as two digits
3. LED bar graph (bargraph1) lights segments equal to the tens digit (e.g., 25 → 2 segments lit) (from pin:A1 to pin:A10)
4. RGB LEDs (rgb1, rgb2) change color based on value ranges:
   - Red: 0-5
   - Green: 6-9
   - Blue: 10-99
5. All components must update simultaneously with each increment
6. If tens digit exceeds 8 (numbers 80-99), bar graph shows maximum 8 lit segments

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,get_sevseg_value, correct_sleep
from untils import sevseg_value

def test(clock, driver, args, deviation=0.2):
   colors = [
       [1,0,0]+[1,0,0],
       [0,1,0]+[0,1,0],
       [0,0,1]+[0,0,1]
   ]
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   cur_index = (cur_time // 2)
   tens = cur_index // 10
   ones = cur_index % 10
   correct = sevseg_value[str(tens)] + sevseg_value[str(ones)]
   if cur_index <= 5:
      correct += colors[0]
   elif cur_index <= 9:
      correct += colors[1]
   else:
      correct += colors[2]
   if tens > 8:
      correct += [1,1,1,1,1,1,1,1,0,0]
   else:
      correct += [1 for _ in range(tens)] + [0 for _ in range(10-tens)]
   current = [*sevseg1_value, *sevseg2_value, *rgb1_value, *rgb2_value,*bargraph1_value]
   return np.allclose(current, correct, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(12.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(22.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res
