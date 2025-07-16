'''

**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) and a 7-segment display (sevseg1) using a shift register (sr1) and two slide potentiometers (pot1, pot2). The RGB LED will display a color based on the values of the two potentiometers, and the 7-segment display will show a number corresponding to the brightness level of the RGB LED.

**Detail Rules**:
Initialization: Upon powering on or resetting, the RGB LED (rgb1) should be off, and the 7-segment display (sevseg1) should show "0".
Potentiometer Interaction:
1. The first potentiometer (pot1) controls the brightness of the red and green components of the RGB LED. The value of pot1 is mapped to a range of 0 to 255 for the red and green components.
2. The second potentiometer (pot2) controls the brightness of the blue component of the RGB LED. The value of pot2 is mapped to a range of 0 to 255 for the blue component.
3. The 7-segment display (sevseg1) should show a number between 0 and 9, representing the average brightness level of the RGB LED. The average brightness is calculated as (red + green + blue) / 3, divided by 28.33 to scale it to a range of 0 to 9.
4. The RGB LED and 7-segment display should update continuously based on the current values of the potentiometers.

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
   if pot_pos == [0,0]:
      correct = [0,0,0] + sevseg_value['0']
   elif pot_pos == [1,0]:
      correct = [1,1,0] + sevseg_value['6']
   elif pot_pos == [0,1]:
      correct = [0,0,1] + sevseg_value['3']
   elif pot_pos == [1,1]:
      correct = [1,1,1] + sevseg_value['9']
   
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   currect_state = [*rgb1_value, *sevseg1_value]

   return np.allclose(currect_state, correct, atol=deviation)

def test_func(driver, clock, args, res):    
   # test 1
   time.sleep(0.5)
   pot_pos = [0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 2
   move_pot(args['pot1'],1,driver)
   pot_pos = [1,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 3
   move_pot(args['pot2'],1,driver)
   pot_pos = [1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 4
   move_pot(args['pot1'],0,driver)
   pot_pos = [0,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)
   return res