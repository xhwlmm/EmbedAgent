'''

**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) using a slide potentiometer (pot1). The potentiometer will select one of eight predefined colors, which the RGB LED should display based on the potentiometer's position.

**Detail Rules**:
1. The RGB LED (rgb1) must display one of eight colors corresponding to the potentiometer's (pot1) value divided into eight equal ranges:
   - **0-127**: All LEDs off  
   - **128-255**: Red  
   - **256-383**: Green  
   - **384-511**: Blue  
   - **512-639**: Red + Green (Yellow)  
   - **640-767**: Red + Blue (Magenta)  
   - **768-895**: Green + Blue (Cyan)  
   - **896-1023**: All LEDs on (White)  
2. The displayed color must update immediately when the potentiometer is adjusted to a new range.

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
   if pot_pos == [0]:
      correct = [0,0,0]
      return np.allclose(correct, get_rgb_value(args['rgb1'], driver), atol=deviation)
   elif pot_pos == [1]:
      correct = [1,1,1]
      return np.allclose(correct, get_rgb_value(args['rgb1'], driver), atol=deviation)
   elif pot_pos == [0.5]:
      correct = [0,0,1],[1,1,0]
      return np.allclose([0,0,1], get_rgb_value(args['rgb1'], driver), atol=deviation) or np.allclose([1,1,0], get_rgb_value(args['rgb1'], driver), atol=deviation)
   

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
