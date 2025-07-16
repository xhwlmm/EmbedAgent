'''

**Task**:
You are tasked with programming an Arduino (uno) to control three RGB LEDs (rgb1, rgb2, rgb3), three servos (servo1, servo2, servo3), and two slide potentiometers (pot1, pot2). The RGB LEDs will display colors based on the values of the potentiometers, and the servos will rotate to positions corresponding to the potentiometer values. The system should dynamically update the colors and servo positions as the potentiometers are adjusted.

**Detail Rules**:
1. **RGB LEDs**:
   - The first potentiometer (pot1) controls the red component of all three RGB LEDs (rgb1, rgb2, rgb3). The value of pot1 is mapped to a range of 0 to 255 for the red component.
   - The second potentiometer (pot2) controls the green component of all three RGB LEDs (rgb1, rgb2, rgb3). The value of pot2 is mapped to a range of 0 to 255 for the green component.
   - The blue component of all three RGB LEDs is fixed at 0 (turned off).
   - The RGB LEDs should update their colors continuously based on the current values of the potentiometers.

2. **Servos**:
   - The first potentiometer (pot1) controls the position of the first servo (servo1). The value of pot1 is mapped to a range of 0 to 180 degrees.
   - The second potentiometer (pot2) controls the position of the second servo (servo2). The value of pot2 is mapped to a range of 0 to 180 degrees.
   - The third servo (servo3) should alternate between 0 and 180 degrees every 2 seconds, independent of the potentiometers.
   - The servos should update their positions continuously based on the current values of the potentiometers or the alternating logic for servo3.

3. **System Behavior**:
   - The RGB LEDs and servos should update their states every 100 milliseconds to ensure smooth transitions.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,get_sevseg_value,correct_sleep
from untils import sevseg_value

def test(clock, driver, pot_pos, args, deviation=0.2):
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_num = (cur_time // 2) % 2
   if pot_pos == [1,0]:
      correct = [1,0,0]*3 + [180,0,180*correct_num]
   elif pot_pos == [1,1]:
      correct = [1,1,0]*3 + [180,180,180*correct_num]
   elif pot_pos == [0,1]:
      correct = [0,1,0]*3 + [0,180,180*correct_num]
   elif pot_pos == [0,0]:
      correct = [0,0,0]*3 + [0,0,180*correct_num]
   servo3_value = get_servo_value(args['servo3'],driver)
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   rgb3_value = get_rgb_value(args['rgb3'], driver)
   currect_state = [*rgb1_value,*rgb2_value,*rgb3_value,servo1_value,servo2_value,servo3_value]
   return np.allclose(currect_state[:-3:], correct[:-3:], atol=deviation) and np.allclose(currect_state[-3:], correct[-3:], atol=1)

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
   correct_sleep(6.5,clock)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 3
   move_pot(args['pot1'],0,driver)
   pot_pos = [0,1]
   correct_sleep(10.5,clock)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 4
   move_pot(args['pot2'],0,driver)
   pot_pos = [0,0]
   correct_sleep(14.6,clock)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   return res
