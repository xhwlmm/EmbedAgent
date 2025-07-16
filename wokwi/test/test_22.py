'''
  
**Task**:  
You are tasked with programming an Arduino (uno) to control the color of an RGB LED (rgb1) using three slide potentiometers (pot1, pot2, pot3). Each potentiometer will independently adjust the intensity of one of the RGB LED's color channels (red, green, or blue), allowing the user to mix colors dynamically.  

**Detail Rules**:  
1. **Initialization**:  
   - The RGB LED (rgb1) must start in an **off state** when the Arduino is powered on or reset.  

2. **Potentiometer Interaction**:  
   - The first potentiometer (pot1) controls the **red** channel intensity.  
   - The second potentiometer (pot2) controls the **green** channel intensity.  
   - The third potentiometer (pot3) controls the **blue** channel intensity.  
   - The analog values from the potentiometers (0-1023) must be mapped to the PWM range (0-255) for controlling the LED brightness.  

3. **LED Behavior**:  
   - The RGB LED (rgb1) must update its color **continuously** based on the current values of the potentiometers.  
   - If all potentiometers are at their minimum value (0), the LED must remain off.  

4. **Hardware Usage**:  
   - All components (Arduino, three potentiometers, RGB LED) must be utilized as described.  

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
   correct = []
   if pot_pos == [1,0,0]:
      correct = [1,0,0]
   elif pot_pos == [1,1,0]:
      correct = [1,1,0]
   elif pot_pos == [1,1,1]:
      correct = [1,1,1]
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   currect_state = [*rgb1_value]
   return np.allclose(correct, currect_state, atol=deviation)

def test_func(driver, clock, args, res):    
   # test 1
   time.sleep(0.5)
   move_pot(args['pot1'],1,driver)
   pot_pos = [1,0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 2
   move_pot(args['pot2'],1,driver)
   pot_pos = [1,1,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 3
   move_pot(args['pot3'],1,driver)
   pot_pos = [1,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   return res
