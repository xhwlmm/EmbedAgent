'''

**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2) and a 10-segment LED bar graph (bargraph1) using a slide potentiometer (pot1) and two shift registers (sr1, sr2). The potentiometer will set a numeric value displayed on the 7-segment displays, while the LED bar graph will visually represent the magnitude of this value.

**Detail Rules**:
1. **Initialization**:  
   - On startup, both 7-segment displays show "00". 
   - the sevseg1 shows the tens digit and sevseg2 shows the units digit.
   - All segments of the LED bar graph (bargraph1) must remain off.  

2. **Potentiometer Control**:  
   - The potentiometer (pot1) determines a value between 0 and 99. This value must be displayed in real-time on the two 7-segment displays, with sevseg1 showing the tens digit and sevseg2 showing the units digit.  
   - The LED bar graph (bargraph1) must light up a number of segments proportional to the potentiometer value. For example:  
     - 0-9: 0 LEDs lit  
     - 10-19: 1 LED lit  
     - ...  
     - 90-99: 9 LEDs lit  

3. **Behavior Constraints**:  
   - The 7-segment displays and LED bar graph must update continuously without noticeable delay as the potentiometer is adjusted.  
   - If the potentiometer is set to its maximum value (99), all 9 LEDs of the bar graph (indices 0-8) must light up.  
   - Ensure the system remains responsive to potentiometer changes at all times.  

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
   bargrah1_value = get_bargraph_value(args['bargraph1'], driver)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
   if pot_pos == [0]:
      correct = sevseg_value['0'] + sevseg_value['0'] + [0]*10
   elif pot_pos == [1]:
      correct = sevseg_value['9'] + sevseg_value['9'] + [1]*10
   current_state = sevseg1_value + sevseg2_value + bargrah1_value
         
   return np.allclose(correct, current_state, atol=deviation)

def test_func(driver, clock, args, res):    
   # test 1
   time.sleep(0.5)
   pot_pos = [0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 2
   move_pot(args['pot1'],1,driver)
   pot_pos = [1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 3
   move_pot(args['pot1'],0,driver)
   pot_pos = [0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   return res