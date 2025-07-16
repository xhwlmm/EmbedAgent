'''

**Task**:
You are tasked with programming an Arduino (uno) to synchronize three servo motors (servo1, servo2, servo3) with a 10-segment LED bar graph (bargraph1). The servos must rotate sequentially to their maximum angle, while the LED bar graph visually indicates the progression of their movements. All components must work in a coordinated sequence.

**Detail Rules**:
1. **Initialization**:  
   - All servos start at 0° (neutral position).  
   - All segments of the LED bar graph (bargraph1) remain off.  

2. **Sequential Activation**:  
   - **Phase 1**:  
     - Servo1 (servo1) rotates to 180° and keep for 2 seconds.  
     - The first 3 segments of the LED bar graph(pin:A1 to pin:A3) light up and stay illuminated for 2 seconds.  
   - **Phase 2**:  
     - Servo2 (servo2) rotates to 180° and keep for 2 seconds.  
     - The next 3 segments of the LED bar graph light up (pin:A1 to pin:A6,total 6 segments) and stay illuminated for 2 seconds.  
   - **Phase 3**:  
     - Servo3 (servo3) rotates to 180° and keep for 2 seconds.  
     - The final 4 segments of the LED bar graph light up (pin:A1 to pin:A10,total 10 segments) and stay illuminated for 2 seconds.  

3. **Reset**:  
   - All servos return to 0° simultaneously.  
   - All LED segments turn off.  
   - The system pauses for 2 seconds before restarting the sequence.  

4. **Timing**:  
   - Each phase (servo movement + LED illumination) must maintain its state for **at least 2 seconds**.  
   - The reset state must also persist for 2 seconds.  

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

def test(clock, driver, args, deviation=0.2):
   servo1_value = get_servo_value(args["servo1"],driver)
   servo2_value = get_servo_value(args["servo2"],driver)
   servo3_value = get_servo_value(args["servo3"],driver)
   bargraph1_value = get_bargraph_value(args["bargraph1"], driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_num = (cur_time // 2) % 4
   if correct_num != 3:
      correct_servo1_value = 180
   else:
      correct_servo1_value = 0
   if correct_num not in [3,0]:
      correct_servo2_value = 180
   else:
      correct_servo2_value = 0
   if correct_num not in [3,0,1]:
      correct_servo3_value = 180
   else:
      correct_servo3_value = 0

   correct_bargraph_value = np.zeros(10)
   if correct_num == 0:
      correct_bargraph_value[0:3] = 1
   elif correct_num == 1:
      correct_bargraph_value[0:6] = 1
   elif correct_num == 2:
      correct_bargraph_value[0:10] = 1
   if abs(servo1_value - correct_servo1_value) <= deviation and abs(servo2_value - correct_servo2_value) <= deviation and abs(servo3_value - correct_servo3_value) <= deviation and np.allclose(bargraph1_value,correct_bargraph_value,deviation):
      return True
   else:
      return False


def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(4.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(6.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    
    # test 4
    correct_sleep(8.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res