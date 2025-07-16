'''

**Task**:
You are tasked with programming an Arduino (uno) to synchronize two servo motors (servo1, servo2) and a 10-segment LED bar graph (bargraph1) using a slide potentiometer (pot1). The potentiometer will control the angular position of both servos and the number of illuminated LEDs in the bar graph simultaneously.

**Detail Rules**:
1. **Initialization**:  
   - Both servos (servo1, servo2) must start at 0° when powered on.  
   - All LEDs in the bar graph (bargraph1) must be off initially.  

2. **Potentiometer Control**:  
   - The slide potentiometer (pot1) value (0-1023) must be linearly mapped to:  
     - Servo angles: 0° (minimum) to 180° (maximum) for servo1, and 180° to 0° for servo2 (opposite direction).  
     - Active LEDs: 0 (all off) to 10 (all on) in the bar graph. (from pin A1 to A10) 

3. **Synchronization**:  
   - When the potentiometer is at 0%:  
     - servo1 = 0°, servo2 = 180°, all LEDs off.  
   - When the potentiometer is at 50%:  
     - servo1 = 90°, servo2 = 90°, exactly 5 LEDs lit.  
   - When the potentiometer is at 100%:  
     - servo1 = 180°, servo2 = 0°, all LEDs lit.  

4. **LED Behavior**:  
   - LEDs must light up sequentially from left to right as the potentiometer value increases.  
   - No flickering or partial brightness is allowed, LEDs must be fully on or off.  

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
   
   servo1 = get_servo_value(args['servo1'],driver)
   servo2 = get_servo_value(args['servo2'],driver)
   bargraph1 = get_bargraph_value(args['bargraph1'], driver)

   if pot_pos == [0]:
      correct = np.array([0,180,0,0,0,0,0,0,0,0,0,0])
   elif pot_pos == [1]:
      correct = np.array([180,0,1,1,1,1,1,1,1,1,1,1])
         
   return np.allclose(correct, [servo1, servo2, *bargraph1], atol=deviation)

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