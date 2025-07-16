'''

**Task**:
Program the Arduino (uno) to control three servo motors (servo1, servo2, servo3) and a 10-segment LED bar graph (bargraph1) using two slide potentiometers (pot1, pot2). The potentiometers adjust the angles of the servos, while the LED bar visually represents the combined input level.

**Detail Rules**:
- **Initialization**: All servos start at 0 degrees, and the LED bar (bargraph1) is completely off.
- **Potentiometer Control**:
  1. pot1 directly controls the angle of servo1 (servo1) from 0 to 180 degrees.
  2. pot2 directly controls the angle of servo2 (servo2) from 0 to 180 degrees.
  3. The average value of pot1 and pot2 (rounded to the nearest integer) determines the angle of servo3 (servo3) from 0 to 180 degrees.
- **LED Bar Display**: The number of lit segments in the LED bar (bargraph1) corresponds to the average value of the two potentiometers, scaled to 0-10 segments (0 = all off, 10 = all on) (The order of the segments is from pin:A1 to pin:A10).

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
      correct = [180,0,90]+[1,1,1,1,1,0,0,0,0,0]
   elif pot_pos == [1,1]:
      correct = [180,180,180]+[1,1,1,1,1,1,1,1,1,1]
   elif pot_pos == [0,1]:
      correct = [0,180,90] + [1,1,1,1,1,0,0,0,0,0]
   elif pot_pos == [0,0]:
      correct = [0,0,0] + [0,0,0,0,0,0,0,0,0,0]
   servo1 = get_servo_value(args['servo1'], driver)
   servo2 = get_servo_value(args['servo2'], driver)
   servo3 = get_servo_value(args['servo3'], driver)
   bargraph1 = get_bargraph_value(args['bargraph1'], driver)
   currect_state = [servo1, servo2, servo3] + bargraph1
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
   driver.save_screenshot('screenshot.png')
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   # test 4
   move_pot(args['pot2'],0,driver)
   pot_pos = [0,0]
   time.sleep(0.5)
   res["msg"].append(1 if test(clock, driver, pot_pos, args) else 0)

   return res