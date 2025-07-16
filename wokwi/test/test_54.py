'''

**Task**:
You are tasked with programming an Arduino (uno) to create an interactive color mixer and visualizer using an RGB LED (rgb1), a slide potentiometer (pot1), and a 10-segment LED bar graph (bargraph1). The potentiometer controls the intensity of individual RGB color components, while the bar graph visually represents the selected intensity level.

**Detail Rules**:
1. **Initialization**:  
   - All components start in an off state when powered on or reset.

2. **Color Mixing**:
   - The potentiometer (pot1) adjusts the brightness of one RGB component (red, green, or blue) at a time, cycling through these three modes automatically every 5 seconds.
   - The RGB LED (rgb1) displays the combined color of the currently active component's intensity (from the potentiometer) and the previous components' intensities.

3. **Bar Graph Display**:
   - The LED bar graph (bargraph1) lights up segments proportional to the potentiometer's value (0-1023 mapped to 0-10 segments).
   - Full intensity (1023) lights all 10 segments, while 0 intensity keeps the bar graph off.

4. **Mode Cycling**:
   - Red mode (first 5 seconds): Adjust red intensity. Previous green/blue intensities persist.
   - Green mode (next 5 seconds): Adjust green intensity. Previous red/blue intensities persist.
   - Blue mode (final 5 seconds): Adjust blue intensity. Previous red/green intensities persist.
   - The cycle repeats indefinitely, with each mode lasting exactly 5 seconds.

5. **Persistence**:
   - Each color mode must maintain its state for the full 5-second duration to allow verification.
   - The bar graph updates continuously to reflect real-time potentiometer values.

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
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
   current = [*rgb1_value ,*bargraph1_value]
   return np.allclose(current, pot_pos, atol=deviation)

def test_func(driver, clock, args, res):    
   # test 1
   time.sleep(0.5)
   move_pot(args['pot1'],1,driver)
   pot_pos = [1,0,0,1,1,1,1,1,1,1,1,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)
   time.sleep(5)
   # test 2
   move_pot(args['pot1'],0,driver)
   pot_pos = [1,0,0,0,0,0,0,0,0,0,0,0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   time.sleep(3)
   # test 3
   move_pot(args['pot1'],1,driver)
   pot_pos = [1,0,1,1,1,1,1,1,1,1,1,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   return res