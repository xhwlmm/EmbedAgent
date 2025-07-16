'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) and three servo motors (servo1, servo2, servo3). The 7-segment display will show a number that increments from 0 to 9, and each servo motor will rotate to a specific angle based on the displayed number. The servos should move in sequence, with each servo completing its movement before the next one starts.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should show "0", and all servos (servo1, servo2, servo3) should be at their initial position (0 degrees).
Display and Servo Interaction:
1. The 7-segment display (sevseg1) will increment its displayed number from 0 to 9, with each number displayed for 2 seconds.
2. When the number changes, the servos will move to specific angles based on the displayed number:
   - For numbers 0-2: servo1 moves to 0 degrees, servo2 to 45 degrees, and servo3 to 90 degrees.
   - For numbers 3-5: servo1 moves to 45 degrees, servo2 to 90 degrees, and servo3 to 135 degrees.
   - For numbers 6-8: servo1 moves to 90 degrees, servo2 to 135 degrees, and servo3 to 180 degrees.
   - For number 9: all servos return to 0 degrees.
3. After reaching 9, the display should reset to 0, and the cycle should repeat.
4. The servos should move immediately and accurately to their target positions.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,get_sevseg_value, correct_sleep
from untils import sevseg_value

def test(clock, driver, args, deviation=0.2):
    servo1_value = get_servo_value(args["servo1"],driver)
    servo2_value = get_servo_value(args["servo2"],driver)
    servo3_value = get_servo_value(args["servo3"],driver)
    sevseg1_value = get_sevseg_value(args["sevseg1"], driver)
    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    correct_num = cur_time // 2
    correct_num = correct_num % 10
    correct_sevseg1_value = sevseg_value[str(correct_num)]
    if np.allclose(correct_sevseg1_value, sevseg1_value, atol=deviation):
        if 2 >= correct_num >= 0:
            if np.allclose(servo1_value, 0, atol=deviation) and np.allclose(servo2_value, 45, atol=deviation) and np.allclose(servo3_value, 90, atol=deviation):
                return True
            else:
                return False
        elif 5 >= correct_num >= 3:
            if np.allclose(servo1_value, 45, atol=deviation) and np.allclose(servo2_value, 90, atol=deviation) and np.allclose(servo3_value, 135, atol=deviation):
                return True
            else:
                return False
        elif 8 >= correct_num >= 6:
            if np.allclose(servo1_value, 90, atol=deviation) and np.allclose(servo2_value, 135, atol=deviation) and np.allclose(servo3_value, 180, atol=deviation):
                return True
            else:
                return False
        elif correct_num == 9:
            if np.allclose(servo1_value, 0, atol=deviation) and np.allclose(servo2_value, 0, atol=deviation) and np.allclose(servo3_value, 0, atol=deviation):
                return True

            else:
                return False
            


def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(0.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(2.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(4.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    
    # test 4
    correct_sleep(12.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 5
    correct_sleep(22.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    

    return res