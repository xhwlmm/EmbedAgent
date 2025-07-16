'''

**Task**:
You are tasked with programming an Arduino (uno) to control three servo motors (servo1, servo2, servo3) using two slide potentiometers (pot1, pot2). The first potentiometer (pot1) will control the angle of the first servo (servo1), while the second potentiometer (pot2) will control the angles of the second and third servos (servo2, servo3) simultaneously. The servos should move smoothly in response to changes in the potentiometer values.

**Detail Rules**:
1. **Servo Control**:
   - The first servo (servo1) should be controlled by the first potentiometer (pot1). The angle of servo1 should range from 0° to 180°, corresponding to the potentiometer's value (0 to 1023).
   - The second and third servos (servo2, servo3) should be controlled by the second potentiometer (pot2). Both servos should move in unison, with their angles ranging from 0° to 180°, corresponding to the potentiometer's value (0 to 1023).

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value

def test_func(driver, clock, args, res): 
    # test 1 
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    servo3_value = get_servo_value(args['servo3'],driver)
    if abs(servo1_value-0) < 1 and abs(servo2_value-0) < 1 and abs(servo3_value-0) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 2
    move_pot(args['pot1'],1,driver)
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    servo3_value = get_servo_value(args['servo3'],driver)
    if abs(servo1_value-180) < 1 and abs(servo2_value-0) < 1 and abs(servo3_value-0) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 3
    move_pot(args['pot2'],1,driver)
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    servo3_value = get_servo_value(args['servo3'],driver)
    if abs(servo1_value-180) < 1 and abs(servo2_value-180) < 1 and abs(servo3_value-180) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 4
    move_pot(args['pot1'],0,driver)
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    servo3_value = get_servo_value(args['servo3'],driver)
    if abs(servo1_value-0) < 1 and abs(servo2_value-180) < 1 and abs(servo3_value-180) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    return res