'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 10-segment LED bar graph (bargraph1) using three slide potentiometers (pot1, pot2, pot3). The potentiometers will define an active range of LEDs and determine how many LEDs within that range are lit.

**Detail Rules**:
1. **Initialization**: All LEDs in the bar graph (bargraph1) must be off when the system starts.
2. **Range Definition**:
   - The first potentiometer (pot1) sets the lower bound of the active range (0-9) of graph (bargraph1). (pins: A1-A10)
   - The second potentiometer (pot2) sets the upper bound of the active range (0-9) of graph (bargraph1). (pins: A1-A10)
3. **Fill Control**:
   - The third potentiometer (pot3) determines the fill percentage (0-100%) within the active range. This percentage dictates how many LEDs between the lower and upper bounds are lit.
4. **Direction Handling**:
   - If the lower bound ≤ upper bound, LEDs light up sequentially from the lower to upper bound (both endpoints inclusive) based on the fill percentage.
   - If the lower bound > upper bound, LEDs light up sequentially from the upper to lower bound (both endpoints inclusive) based on the fill percentage.
5. **Display Update**:
   - The LED bar graph updates continuously to reflect changes in potentiometer values.

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
   if pot_pos[2] == 0:
      correct = np.array([0,0,0,0,0,0,0,0,0,0])
   else:
      if pot_pos[0] == 1 and pot_pos[1] == 1:
         correct = np.array([0,0,0,0,0,0,0,0,0,1])
      if pot_pos[0] == 0 and pot_pos[1] == 0:
         correct = np.array([1,0,0,0,0,0,0,0,0,0])
      if pot_pos[0] == 0 and pot_pos[1] == 1:
         correct = np.array([1,1,1,1,1,1,1,1,1,1])
      if pot_pos[0] == 1 and pot_pos[1] == 0:
         correct = np.array([1,1,1,1,1,1,1,1,1,1])
   currect_state = get_bargraph_value(args['bargraph1'], driver)
         
   return np.allclose(correct, currect_state, atol=deviation)

def test_func(driver, clock, args, res):    
   # test 1
   time.sleep(0.5)
   move_pot(args['pot2'],1,driver)
   pot_pos = [0,1,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 2
   move_pot(args['pot3'],1,driver)
   pot_pos = [0,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 3
   move_pot(args['pot1'],1,driver)
   pot_pos = [1,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 4
   move_pot(args['pot2'],0,driver)
   pot_pos = [1,0,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 5
   move_pot(args['pot1'],0,driver)
   pot_pos = [0,0,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   return res
