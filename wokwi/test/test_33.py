'''

**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2) and three servo motors (servo1, servo2, servo3). The 7-segment displays will show a two-digit number, where one display represents the tens digit and the other represents the units digit. The servos will rotate to specific angles based on the displayed number. The number will increment every 2 seconds, and the servos will update their positions accordingly.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00", and all servos (servo1, servo2, servo3) should be at their 0-degree position.
Number Increment: Every 2 seconds, the displayed number should increment by 1. If the number exceeds 99, it should reset to 0.
Servo Control: The servos should rotate to specific angles based on the displayed number:
- Servo1 (servo1) should rotate to an angle equal to the displayed number multiplied by 1.8 (e.g., for number 10, the angle is 18 degrees).
- Servo2 (servo2) should rotate to an angle equal to the displayed number multiplied by 1.2 (e.g., for number 10, the angle is 12 degrees).
- Servo3 (servo3) should rotate to an angle equal to the displayed number multiplied by 0.6 (e.g., for number 10, the angle is 6 degrees).
Display Update: The 7-segment displays should immediately update to reflect the new number after each increment.
Servo Update: The servos should immediately update their positions to the new angles after each number increment.

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
    sevseg1_value = get_sevseg_value(args["sevseg1"], driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"], driver)
    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    correct_num = cur_time // 2
    correct_sevseg1_value = sevseg_value[str(correct_num // 10)]
    correct_sevseg2_value = sevseg_value[str(correct_num % 10)]
    correct_servo1_value = correct_num * 1.8
    correct_servo2_value = correct_num * 1.2
    correct_servo3_value = correct_num * 0.6
    if abs(servo1_value - correct_servo1_value) < 1 and abs(servo2_value - correct_servo2_value) < 1 and abs(servo3_value - correct_servo3_value) < 1 and np.allclose(sevseg1_value, correct_sevseg1_value, atol=deviation) and np.allclose(sevseg2_value, correct_sevseg2_value, atol=deviation):
        return True
    else:
        return False


def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(10.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    
    # test 4
    correct_sleep(14.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 5
    correct_sleep(24.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    

    return res