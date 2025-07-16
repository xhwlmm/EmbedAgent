'''
  
**Task**:  
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) using three pushbuttons (btn1, btn2, btn3) and three slide potentiometers (pot1, pot2, pot3). Each button corresponds to a color channel (red, green, blue), and its associated potentiometer adjusts the intensity of that color. The RGB LED must display the combined color based on the selected channels.  

**Detail Rules**:  
1. **Initialization**: The RGB LED (rgb1) starts in an off state (all color channels at 0).  
2. **Button Interaction**:  
   - Pressing **btn1** activates the red channel. While held, the red intensity is controlled by **pot1** (0-255).  
   - Pressing **btn2** activates the green channel. While held, the green intensity is controlled by **pot2** (0-255).  
   - Pressing **btn3** activates the blue channel. While held, the blue intensity is controlled by **pot3** (0-255).  
3. **Real-Time Adjustment**: While a button is held, the corresponding potentiometer updates its color intensity continuously. The RGB LED (rgb1) reflects these changes immediately.  
4. **State Retention**: Releasing a button locks the current intensity of its associated color channel. The LED maintains the combined color until another adjustment is made.  
5. **Debouncing**: Each button press must be debounced to avoid false triggers (0.15-second press duration).  

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
   time.sleep(0.5)
   move_pot(args['pot2'], 1, driver)
   time.sleep(0.5)
   move_pot(args['pot3'], 1, driver)
   correct_answer = [0,0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   # test 2: click the button
   click_button(args['btn1'], actions)
   time.sleep(0.5)
   correct_answer = [1,0,0]
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)

   # test 3: click the button twice
   click_button(args['btn2'], actions)
   time.sleep(0.5)
   correct_answer = [1,1,0]
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)

   # test 4: click the button three times
   click_button(args['btn3'], actions)
   time.sleep(0.5)
   correct_answer = [1,1,1]
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)

   # test 5
   move_pot(args['pot1'], 0, driver)
   time.sleep(0.5)
   move_pot(args['pot2'], 0, driver)
   time.sleep(0.5)
   move_pot(args['pot3'], 0, driver)
   time.sleep(0.5)
   correct_answer = [1,1,1]
   res["msg"].append(1 if test(correct_answer, args, driver) else 0)
   return res