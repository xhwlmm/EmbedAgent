'''

**Task**:
You are tasked with programming an Arduino (uno) to control the colors of two RGB LEDs (rgb1, rgb2) using two slide potentiometers (pot1, pot2). The first potentiometer (pot1) will control the color of the first RGB LED (rgb1), while the second potentiometer (pot2) will control the color of the second RGB LED (rgb2). The potentiometers will determine the hue of the RGB LEDs, and the colors should change smoothly as the potentiometers are adjusted.

**Detail Rules**:
1. **Initialization**: Upon powering on or resetting, both RGB LEDs (rgb1, rgb2) should be off.
2. **Potentiometer Interaction**:
   - The first potentiometer (pot1) will control the hue of the first RGB LED (rgb1). The value of pot1 (0 to 1023) will be mapped to a hue value between 0 and 360 degrees.
   - The second potentiometer (pot2) will control the hue of the second RGB LED (rgb2). The value of pot2 (0 to 1023) will also be mapped to a hue value between 0 and 360 degrees.
3. **Color Calculation**:
   - The hue value from each potentiometer will be converted to RGB values using the HSV-to-RGB conversion algorithm.
   - The saturation and value (brightness) of the RGB values will be set to 1 (maximum saturation brightness).
   - The RGB values will be used to set the brightness of the corresponding RGB LED.
4. **LED Update**:
   - The colors of the RGB LEDs should update continuously as the potentiometers are adjusted.
5. **Smooth Transition**:
   - The transition between colors should be smooth, with no abrupt changes in brightness or color.

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
   correct = []
   if pot_pos == [1,0]:
      correct = [1,1,0] + [1,0,0]
   elif pot_pos == [1,1]:
      correct = [1,1,0] + [1,1,0]
   elif pot_pos == [0,1]:
      correct = [1,0,0] + [1,1,0]
   elif pot_pos == [0,0]:
      correct = [1,0,0] + [1,0,0]
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   currect_state = [*rgb1_value,*rgb2_value]
   return np.allclose(correct, currect_state, atol=deviation)

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
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 3
   move_pot(args['pot1'],0,driver)
   pot_pos = [0,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 4
   move_pot(args['pot2'],0,driver)
   pot_pos = [0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   return res