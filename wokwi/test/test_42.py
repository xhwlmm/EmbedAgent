'''

**Task**:
You are tasked with programming an Arduino (uno) to control a system that includes two 7-segment displays (sevseg1, sevseg2), a 10-segment LED bar graph (bargraph1), and three servos (servo1, servo2, servo3). The 7-segment displays will show a two-digit number, the LED bar graph will visually represent the number's value, and the servos will rotate to specific angles based on the number. The number will increment by 1 every 2 seconds, and the system should update all components accordingly.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00", the LED bar graph should be off, and all servos should be at 0 degrees.
Number Increment: Every 2 seconds, the number displayed on the 7-segment displays should increment by 1. If the number exceeds 99, it should reset to 0.
LED Bar Graph: The LED bar graph (bargraph1) should light up a number of LEDs equal to the tens digit of the current number. For example, if the number is 37, 3 LEDs should be lit.
Servo Control: The servos (servo1, servo2, servo3) should rotate to angles based on the units digit of the current number. The angle for each servo is calculated as follows:
- servo1: units digit * 18 degrees
- servo2: units digit * 18 degrees + 60 degrees
- servo3: units digit * 18 degrees + 120 degrees
When sevseg displays 9, hold this state for 2 seconds, then rotate servo 1, servo 2, servo 3 to 0 degrees.
Display Update: The 7-segment displays, LED bar graph, and servos should update immediately after each number increment.

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
    bar1_value = get_bargraph_value(args["bargraph1"], driver)
    sevseg1_value = get_sevseg_value(args["sevseg1"], driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"], driver)
    servo1_value = get_servo_value(args["servo1"],driver)
    servo2_value = get_servo_value(args["servo2"],driver)
    servo3_value = get_servo_value(args["servo3"],driver)
    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    correct_num = cur_time // 2
    correct_sevseg1_value = sevseg_value[str(correct_num // 10)]
    correct_sevseg2_value = sevseg_value[str(correct_num % 10)]
    digit = correct_num % 10
    correct_servo1_value = min(180,digit * 18)
    correct_servo2_value = min(180,digit * 18 + 60)
    correct_servo3_value = min(180,digit * 18 + 120)
    correct_bar1_value = [1 if i < correct_num // 10 else 0 for i in range(10)]
    # print(correct_sevseg1_value, correct_sevseg2_value, correct_bar1_value, correct_servo1_value, correct_servo2_value, correct_servo3_value)
    # print(sevseg1_value, sevseg2_value, bar1_value, servo1_value, servo2_value, servo3_value)
    if abs(servo1_value - correct_servo1_value) < 1 and abs(servo2_value - correct_servo2_value) < 1 and abs(servo3_value - correct_servo3_value) < 1 and np.allclose(sevseg1_value, correct_sevseg1_value, atol=deviation) and np.allclose(sevseg2_value, correct_sevseg2_value, atol=deviation) and np.allclose(bar1_value, correct_bar1_value, atol=deviation):
        return True
    else:
        return False


def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(10,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    
    # test 4
    correct_sleep(14,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 5
    correct_sleep(24,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    

    return res