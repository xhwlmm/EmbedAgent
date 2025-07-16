'''

**Task**:
You are tasked with programming an Arduino (uno) to control two RGB LEDs (rgb1, rgb2), three servos (servo1, servo2, servo3), and a slide potentiometer (pot1). The slide potentiometer will control the color of the RGB LEDs and the positions of the servos. The RGB LEDs will display a color gradient based on the potentiometer's value, and the servos will rotate to positions corresponding to the potentiometer's value.

**Detail Rules**:
1. **RGB LEDs (rgb1, rgb2)**:
   - The potentiometer's value (0 to 1023) will determine the color of the RGB LEDs.
   - The red, green, and blue components of the RGB LEDs will be mapped to the potentiometer's value as follows:
     - Red: Increases from 0 to 255 as the potentiometer value increases from 0 to 341.
     - Green: Increases from 0 to 255 as the potentiometer value increases from 342 to 682.
     - Blue: Increases from 0 to 255 as the potentiometer value increases from 683 to 1023.
   - Both RGB LEDs (rgb1, rgb2) should display the same color at all times.

2. **Servos (servo1, servo2, servo3)**:
   - The potentiometer's value will determine the angle of each servo.
   - The servos will rotate to angles mapped from the potentiometer's value (0 to 1023) to a range of 0 to 180 degrees.
   - Each servo should maintain its position for at least 2 seconds before updating to a new position.

3. **Potentiometer (pot1)**:
   - The potentiometer's value will be read continuously, and the RGB LEDs and servos will update their states accordingly.
   - The system should respond immediately to changes in the potentiometer's value.

4. **Initialization**:
   - On startup, the RGB LEDs should display a color corresponding to the potentiometer's initial value, and the servos should move to their initial positions.


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
   correct = []
   if pot_pos == [0]:
      correct = [0,0,0]*2 + [0]*3
   elif pot_pos == [0.5]:
      correct = [1,1,0]*2 + [90] *3
   elif pot_pos == [1]:
      correct = [1,1,1]*2 + [180] *3
   
   servo3_value = get_servo_value(args['servo3'],driver)
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   currect_state = [*rgb1_value,*rgb2_value,servo1_value,servo2_value,servo3_value]
   return np.allclose(currect_state[:-3:], correct[:-3:], atol=deviation) and np.allclose(currect_state[-3:], correct[-3:], atol=5)

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