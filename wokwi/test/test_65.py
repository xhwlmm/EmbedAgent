'''
  
**Task**:  
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) using a push button (btn1). The RGB LED will cycle through predefined colors each time the button is pressed, with each color state lasting at least 2 seconds.  

**Detail Rules**:  
1. **Initialization**:  
   - The RGB LED (rgb1) must start in an **off state** (all color channels disabled).  

2. **Button Interaction**:  
   - Each valid press of the button (btn1) must cycle the RGB LED (rgb1) through the following sequence:  
     - **Red** → **Green** → **Blue** → **Yellow (Red+Green)** → **Cyan (Green+Blue)** → **Magenta (Red+Blue)** → **White (Red+Green+Blue)** → **Off** → **Repeat**.  
   - A valid button press is defined as holding the button for **at least 0.15 seconds** to avoid false triggers.  
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
    rgb1_value = get_rgb_value(args['rgb1'], driver)
    return np.allclose(rgb1_value, correct_answer, atol=deviation)

        


def test_func(driver, clock, args, res):
   actions = ActionChains(driver)
   # test 1: init
   click_button(args['btn1'], actions)
   correct_answer = [1,0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   # test 2: click the button
   for i in range(3):
      click_button(args['btn1'], actions)
      time.sleep(0.5)
   correct_answer = [1,1,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)

   # test 3: click the button twice
   for i in range(9):
      click_button(args['btn1'], actions)
      time.sleep(0.5)
   correct_answer = [0,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   return res
