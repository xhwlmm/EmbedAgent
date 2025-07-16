'''

**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) using a push button (btn1) and a slide potentiometer (pot1). The RGB LED's color channels (Red, Green, Blue) are cycled through with each button press, and the potentiometer adjusts the brightness of the currently selected color channel.

**Detail Rules**:
1. **Initialization**: Upon powering on or resetting, the RGB LED (rgb1) must remain off.
2. **Button Interaction**:
   - Each debounced press of the button (btn1) cycles through the RGB channels in the order: Red → Green → Blue → Red...
   - The first button press activates the Red channel, subsequent presses cycle to the next channel.
3. **Brightness Control**:
   - The slide potentiometer (pot1) adjusts the brightness of the currently selected color channel (0-255).
   - Unselected channels must remain off.
4. **State Stability**:
   - The RGB LED updates continuously as the potentiometer is adjusted.

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
   move_pot(args['pot1'], 1, driver)
   correct_answer = [0,0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   # test 2: click the button
   click_button(args['btn1'], actions)
   time.sleep(0.5)
   correct_answer = [1,0,0]
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)

   # test 3: click the button twice
   click_button(args['btn1'], actions)
   time.sleep(0.5)
   correct_answer = [0,1,0]
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)

   # test 4: click the button three times
   click_button(args['btn1'], actions)
   time.sleep(0.5)
   correct_answer = [0,0,1]
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)

   # test 5
   move_pot(args['pot1'], 0, driver)
   time.sleep(0.5)
   correct_answer = [0,0,0]
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   return res