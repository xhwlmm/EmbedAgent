'''

**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) using two pushbuttons (btn1, btn2). The buttons allow navigation through a predefined sequence of colors, with btn1 advancing to the next color and btn2 returning to the previous color. The RGB LED must display the selected color continuously until a new button press occurs.

**Detail Rules**:
1. **Initialization**: The RGB LED (rgb1) starts in the **off** state when the system is powered on or reset.
2. **Color Sequence**: The predefined color sequence is:  
   **Off → Red → Green → Blue → Yellow → Cyan → Magenta → White → Off** (looping).
3. **Button Interaction**:
   - Pressing btn1 advances to the **next** color in the sequence.
   - Pressing btn2 returns to the **previous** color in the sequence.
   - The RGB LED must update immediately after a valid button press.
4. **Debouncing**: Button presses must be debounced to avoid false triggers from mechanical vibrations.

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
   click_button(args['btn2'], actions)
   correct_answer = [1,1,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   # test 2: click the button
   for i in range(3):
      click_button(args['btn1'], actions)
      time.sleep(0.5)
   correct_answer = [0,1,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)

   # test 3: click the button twice
   for i in range(9):
      click_button(args['btn1'], actions)
      time.sleep(0.5)
   correct_answer = [0,0,1]
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   return res