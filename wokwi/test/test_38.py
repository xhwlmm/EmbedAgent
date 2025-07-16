'''

**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2), two slide potentiometers (pot1, pot2), and two servo motors (servo1, servo2). The 7-segment displays will show a two-digit number, where one display represents the tens digit (pot1) and the other represents the units digit (pot2). The slide potentiometers will control the angle of the two servo motors (sr1 for servo1, sr2 for servo2), and the 7-segment displays will show the corresponding angles of servo1 in degrees (0-99). The servos should move smoothly to the angles set by the potentiometers, and the displays should update in real-time.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00", and both servo motors (servo1, servo2) should be at their 0-degree position.
Potentiometer Interaction:
1. The first potentiometer (pot1) controls the angle of the first servo motor (servo1). The value of pot1 is mapped to a range of 0 to 99 degrees.
2. The second potentiometer (pot2) controls the angle of the second servo motor (servo2). The value of pot2 is also mapped to a range of 0 to 99 degrees.
Display Update: The 7-segment displays should show the current angles of servo1. The tens digit should be displayed on one display (sevseg1), and the units digit should be displayed on the other display (sevseg2).
Servo Movement: The servo motors should move smoothly to the angles set by the potentiometers. The movement should be updated continuously based on the potentiometer values.

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
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
    if np.allclose(sevseg1_value,sevseg_value['0'],rtol=deviation) and np.allclose(sevseg2_value,sevseg_value['0'],rtol=deviation) and abs(servo1_value-0) < 1 and abs(servo2_value-0) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 2
    move_pot(args['pot1'],1,driver)
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
    if np.allclose(sevseg1_value,sevseg_value['9'],rtol=deviation) and np.allclose(sevseg2_value,sevseg_value['9'],rtol=deviation) and abs(servo1_value-99) < 1 and abs(servo2_value-0) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 3
    move_pot(args['pot2'],1,driver)
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
    if np.allclose(sevseg1_value,sevseg_value['9'],rtol=deviation) and np.allclose(sevseg2_value,sevseg_value['9'],rtol=deviation) and abs(servo1_value-99) < 1 and abs(servo2_value-99) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 4
    move_pot(args['pot1'],0,driver)
    time.sleep(0.5)
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
    if np.allclose(sevseg1_value,sevseg_value['0'],rtol=deviation) and np.allclose(sevseg2_value,sevseg_value['0'],rtol=deviation) and abs(servo1_value-0) < 1 and abs(servo2_value-99) < 1:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    return res
