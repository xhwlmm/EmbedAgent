'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) using a shift register (sr1) and two slide potentiometers (pot1, pot2). The 7-segment display will show a number between 0 and 9, which is determined by the combined values of the two potentiometers. The first potentiometer (pot1) will control the tens digit, and the second potentiometer (pot2) will control the units digit. The displayed number will be the sum of the mapped values of the two potentiometers.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should show "0".
Potentiometer Interaction:
1. The first potentiometer (pot1) will control the first digit. Its value (0 to 1023) will be mapped to a range of 0 to 9.
2. The second potentiometer (pot2) will control the second digit. Its value (0 to 1023) will also be mapped to a range of 0 to 9.
3. The displayed number on the 7-segment display will be the sum of the mapped values of the two potentiometers.
4. If the sum exceeds 9, the display should show the last digit of the sum (e.g., 12 → 2, 15 → 5).
5. The display should update continuously based on the current values of the potentiometers.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_sevseg_value
from untils import sevseg_value

def test_func(driver, clock, args, res): 
   deviation=0.2
   # test 1 
   time.sleep(0.5)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   if np.allclose(sevseg1_value,sevseg_value['0'],rtol=deviation):
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   # test 2
   move_pot(args['pot1'],1,driver)
   time.sleep(0.5)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   if np.allclose(sevseg1_value,sevseg_value['9'],rtol=deviation):
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   # test 3
   move_pot(args['pot2'],1,driver)
   time.sleep(0.5)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   if np.allclose(sevseg1_value,sevseg_value['8'],rtol=deviation):
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   # test 4
   move_pot(args['pot1'],0,driver)
   time.sleep(0.5)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   if np.allclose(sevseg1_value,sevseg_value['9'],rtol=deviation):
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   return res