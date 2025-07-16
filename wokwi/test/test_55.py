'''

**Task**:
You are tasked with programming an Arduino (uno) to control two RGB LEDs (rgb1, rgb2) using two slide potentiometers (pot1, pot2) and display the combined intensity on an LED bar graph (bargraph1). Each potentiometer selects a primary color (red, green, or blue) for its corresponding RGB LED, while the bar graph shows the average intensity of both potentiometers.

**Detail Rules**:
1. **Initialization**: All components start in an off state when powered on.
2. **RGB Control**:
   - The first potentiometer (pot1) controls the color of the first RGB LED (rgb1). When pot1 is in the lower third of its range (0–340), rgb1 displays red; in the middle third (341–681), green; and in the upper third (682–1023), blue.
   - The second potentiometer (pot2) controls the color of the second RGB LED (rgb2) using the same logic as pot1.
3. **Bar Graph Display**:
   - The LED bar graph (bargraph1) lights up a number of LEDs proportional to the average value of both potentiometers. For example, if the average is 512 (half of 1023), 4 LEDs will light up.
   - The bar graph must update continuously and maintain each state for at least 2 seconds if the potentiometers remain stationary.
4. **Real-Time Updates**: The RGB LEDs and bar graph must update immediately when the potentiometers are adjusted.

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
   correct_num = (cur_time // 2) % 2
   if pot_pos == [1,0]:
      correct = [0,0,1] + [1,0,0] + [1,1,1,1,0,0,0,0,0,0]
   elif pot_pos == [1,1]:
      correct = [0,0,1] + [0,0,1] + [1,1,1,1,1,1,1,1,0,0]
   elif pot_pos == [0,1]:
      correct = [1,0,0] + [0,0,1] + [1,1,1,1,0,0,0,0,0,0]
   elif pot_pos == [0,0]:
      correct = [1,0,0] + [1,0,0] + [0,0,0,0,0,0,0,0,0,0]
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
   current = [*rgb1_value ,*rgb2_value ,*bargraph1_value]
   return np.allclose(current, correct, atol=deviation)

def test_func(driver, clock, args, res):    
   # test 1
   time.sleep(0.5)
   move_pot(args['pot1'],1,driver)
   pot_pos = [1,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 2
   move_pot(args['pot2'],1,driver)
   pot_pos = [1,1]
   time.sleep(2.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 3
   move_pot(args['pot1'],0,driver)
   pot_pos = [0,1]
   time.sleep(2)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 4
   move_pot(args['pot2'],0,driver)
   pot_pos = [0,0]
   time.sleep(1)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   return res