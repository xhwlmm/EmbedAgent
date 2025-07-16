'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) and three servo motors (servo1, servo2, servo3) using a shift register (sr1) and two slide potentiometers (pot1, pot2). The 7-segment display will show a number between 0 and 9, which is determined by the value of the first potentiometer (pot1). The three servo motors will rotate to angles determined by the second potentiometer (pot2), with each servo representing a different range of angles.

**Detail Rules**:
1. **7-Segment Display**:
   - The 7-segment display (sevseg1) should show a number between 0 and 9, mapped from the value of the first potentiometer (pot1). The value of pot1 ranges from 0 to 1023, and it should be mapped to a number between 0 and 9.
   - The displayed number should update continuously as the potentiometer is adjusted.

2. **Servo Motors**:
   - The second potentiometer (pot2) controls the angles of the three servo motors (servo1, servo2, servo3).
   - The value of pot2 ranges from 0 to 1023 and should be mapped to angles as follows:
     - Servo1 (servo1): 0° to 90°.
     - Servo2 (servo2): 90° to 180°.
     - Servo3 (servo3): 180° to 270° (if the servo supports it, otherwise clamp to 180°).
   - The servos should move smoothly to their respective angles as the potentiometer is adjusted.

3. **State Maintenance**:
   - Each state of the 7-segment display and servo motors should be maintained for at least 2 seconds to allow for verification.

4. **Hardware Usage**:
   - All components (7-segment display, shift register, potentiometers, and servos) must be used in the solution.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_sevseg_value
from untils import sevseg_value

def test_func(driver, clock, args, res): 
   deviation=0.2
   # test 1 
   time.sleep(0.5)
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   servo3_value = get_servo_value(args['servo3'],driver)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   if np.allclose(sevseg1_value,sevseg_value['0'],rtol=deviation) and abs(servo1_value-0) < 1 and abs(servo2_value-90) < 1 and abs(servo3_value-180) < 1:
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   # test 2
   move_pot(args['pot1'],1,driver)
   time.sleep(0.5)
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   servo3_value = get_servo_value(args['servo3'],driver)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   if np.allclose(sevseg1_value,sevseg_value['9'],rtol=deviation) and abs(servo1_value-0) < 1 and abs(servo2_value-90) < 1 and abs(servo3_value-180) < 1:
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   # test 3
   move_pot(args['pot2'],1,driver)
   time.sleep(0.5)
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   servo3_value = get_servo_value(args['servo3'],driver)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   if np.allclose(sevseg1_value,sevseg_value['9'],rtol=deviation) and abs(servo1_value-90) < 1 and abs(servo2_value-180) < 1 and abs(servo3_value-180) < 1:
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   # test 4
   move_pot(args['pot1'],0,driver)
   time.sleep(0.5)
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   servo3_value = get_servo_value(args['servo3'],driver)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   if np.allclose(sevseg1_value,sevseg_value['0'],rtol=deviation) and abs(servo1_value-90) < 1 and abs(servo2_value-180) < 1 and abs(servo3_value-180) < 1:
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   return res
