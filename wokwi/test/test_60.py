'''

**Task**:
You are tasked with programming an Arduino (uno) to control two RGB LEDs (rgb1, rgb2), two 7-segment displays (sevseg1, sevseg2), and three slide potentiometers (pot1, pot2, pot3). The RGB LEDs will display colors based on the values of the potentiometers, while the 7-segment displays will show the corresponding RGB values as two-digit numbers. The first display (sevseg1) will show the red and green values, and the second display (sevseg2) will show the blue value.

**Detail Rules**:
1. **RGB LED Control**:
   - The first potentiometer (pot1) controls the red component of both RGB LEDs (rgb1, rgb2).
   - The second potentiometer (pot2) controls the green component of both RGB LEDs (rgb1, rgb2).
   - The third potentiometer (pot3) controls the blue component of both RGB LEDs (rgb1, rgb2).
   - The RGB values are mapped from the potentiometer readings (0-1023) to a range of 0-255.

2. **7-Segment Display**:
   - The first 7-segment display (sevseg1) will show the red value map 0-255 to 0-9.
   - The second 7-segment display (sevseg2) will show the blue value map 0-255 to 0-9.
   - The displays should update continuously to reflect the current RGB values.



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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,get_sevseg_value
from untils import sevseg_value

def test(clock, driver, pot_pos, args, deviation=0.2):
   correct = []
   if pot_pos == [0,0,0]:
      correct = [0,0,0]*2 + sevseg_value['0'] + sevseg_value['0']
   elif pot_pos == [1,0,0]:
      correct = [1,0,0]*2 + sevseg_value['9'] + sevseg_value['0']
   elif pot_pos == [1,1,0]:
      correct = [1,1,0]*2 + sevseg_value['9'] + sevseg_value['0']
   elif pot_pos == [1,1,1]:
      correct = [1,1,1]*2 + sevseg_value['9'] + sevseg_value['9']
   
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   currect_state = [*rgb1_value,*rgb2_value,*sevseg1_value,*sevseg2_value]

   return np.allclose(currect_state, correct, atol=deviation)

def test_func(driver, clock, args, res):    
   # test 1
   time.sleep(0.5)
   pot_pos = [0,0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 2
   move_pot(args['pot1'],1,driver)
   pot_pos = [1,0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 3
   move_pot(args['pot2'],1,driver)
   pot_pos = [1,1,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 4
   move_pot(args['pot3'],1,driver)
   pot_pos = [1,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)
   return res