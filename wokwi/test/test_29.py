'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 10-segment LED bar graph (bargraph1) using three slide potentiometers (pot1, pot2, pot3). Each potentiometer controls the number of lit LEDs in a specific section of the bar graph, creating a dynamic visual representation of the analog inputs.

**Detail Rules**:
1. **Section Division**:
   - The LED bar graph is divided into three sections:
     - Section 1: First 3 LEDs (controlled by pot1)
     - Section 2: Next 3 LEDs (controlled by pot2)
     - Section 3: Last 4 LEDs (controlled by pot3)
2. **LED Activation**:
   - Each potentiometer’s value (0-1023) determines the number of LEDs lit in its respective section:
     - pot1: 0-1023 maps to 0-3 LEDs in Section 1 (pin A1-A3)
     - pot2: 0-1023 maps to 0-3 LEDs in Section 2 (pin A4-A6)
     - pot3: 0-1023 maps to 0-4 LEDs in Section 3 (pin A7-A10)
   - LEDs in each section must light up sequentially from the first LED of the section. For example, if pot1 is set to light 2 LEDs, the first two LEDs of Section 1 should be on.
3. **Update Behavior**:
   - The display updates continuously to reflect the current potentiometer values.
4. **Initial State**:
   - All LEDs must be off when the system starts or resets.

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
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_bargraph_value = np.zeros(10)
   if pot_pos[0] == 1:
      correct_bargraph_value[0:3] = 1
   if pot_pos[1] == 1:
      correct_bargraph_value[3:6] = 1
   if pot_pos[2] == 1:
      correct_bargraph_value[6:10] = 1
   
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)

   return np.allclose(correct_bargraph_value, bargraph1_value, atol=deviation)

def test_func(driver, clock, args, res):    
   # test 1
   time.sleep(0.5)
   move_pot(args['pot3'],1,driver)
   pot_pos = [0,0,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 2
   move_pot(args['pot2'],1,driver)
   pot_pos = [0,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 3
   move_pot(args['pot1'],1,driver)
   pot_pos = [1,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   return res