'''

**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) using two push buttons (btn1, btn2) and a slide potentiometer (pot1). The RGB LED will cycle through different colors based on the state of the buttons and the value of the potentiometer. The potentiometer will control the brightness of the RGB LED, while the buttons will determine the color mode.

**Detail Rules**:
Initialization: Upon powering on or resetting, the RGB LED (rgb1) should be initialized to red.
Button Interaction:
1. The first button (btn1) will cycle through the red, green, and blue colors of the RGB LED. Each press of btn1 will change the color in the sequence: red → green → blue → red.
2. The second button (btn2) will cycle through the secondary colors (yellow, cyan, magenta) of the RGB LED. Each press of btn2 will change the color in the sequence: yellow → cyan → magenta → yellow.
3. If the RGB LED is in first mode (red, green, blue) and btn2 is pressed, the RGB LED will turn off. If the RGB LED is in second mode (yellow, cyan, magenta) and btn1 is pressed, the RGB LED will turn off.
Potentiometer Interaction:
1. The slide potentiometer (pot1) will control the brightness of the RGB LED. The value of the potentiometer (0 to 1023) will be mapped to a brightness level (0 to 255).
2. The brightness level should be updated continuously based on the current value of the potentiometer.
State Maintenance:
1. The brightness level should be updated in real-time as the potentiometer is adjusted.

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
from untils import sevseg_value,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,get_bargraph_value,click_button,get_servo_value


def test(clock, driver, args, correct, deviation = 0.2):
   rgb1_value = get_rgb_value(args["rgb1"],driver)
   current = [*rgb1_value]
   return np.allclose(current, correct, deviation)



def test_func(driver, clock, args, res):
   actions = ActionChains(driver)
   # test 1: init 
   time.sleep(1)

   # test 2: click the button1 
   bnt_num = [1,0]
   pot = 0
   click_button(args['btn1'], actions)
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, args, [0,0,0]) else 0)

   # test 3: click the button2 
   move_pot(args['pot1'], 1, driver)
   pot = 1
   bnt_num = [2,0]
   click_button(args['btn1'], actions)
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, args, [0,0,1]) else 0)

   # test 4: 
   bnt_num = [3,0]
   click_button(args['btn1'], actions)
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, args, [1,0,0]) else 0)

   bnt_num = [3,1]
   click_button(args['btn2'], actions)
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, args, [0,0,0]) else 0)

   bnt_num = [3,2]
   click_button(args['btn2'], actions)
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, args, [1,1,0]) else 0)

   return res