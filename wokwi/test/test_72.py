'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 10-segment LED bar graph (bargraph1) using a push button (btn1). The bar graph will display a progress level that increases with each button press, cycling from 0 to 10 lit LEDs and then resetting.

**Detail Rules**:
1. **Initialization**:  
   - All LEDs in the bar graph (bargraph1) must be off when the system starts or resets.

2. **Button Interaction**:  
   - Each valid press of the button (btn1) increases the number of lit LEDs by 1.  
   - After reaching 10 lit LEDs, the next press resets the display to 0 lit LEDs.  

3. **Debouncing**:  
   - The button must ignore mechanical vibrations by enforcing a **0.15-second** debounce period.  

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,get_bargraph_value,sevseg_value,get_sevseg_value,click_button,get_servo_value

def test(correct_answer, args, driver, deviation=0.2):
    bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
    return np.allclose(bargraph1_value, correct_answer, atol=deviation)

        


def test_func(driver, clock, args, res):
   actions = ActionChains(driver)
   # test 1: init
   click_button(args['btn1'], actions)
   correct_answer = [1]*1+[0]*9
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   # test 2: click the button
   for i in range(3):
      click_button(args['btn1'], actions)
      time.sleep(0.5)
   correct_answer = [1]*4+[0]*6
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)

   # test 3: click the button twice
   for i in range(9):
      click_button(args['btn1'], actions)
      time.sleep(0.5)
   correct_answer = [1]*2+[0]*8
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   return res
