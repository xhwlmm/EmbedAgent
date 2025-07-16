'''

**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2), a 10-segment LED bar graph (bargraph1), and two servo motors (servo1, servo2). The 7-segment displays will show a two-digit number, the LED bar graph will visually represent the number as a percentage (0-100%), and the servo motors will rotate to positions corresponding to the number. The number will increment every 2 seconds, and the system should reset to 0 after reaching 99.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00", the LED bar graph should be off, and both servo motors should be at their 0-degree position.
Number Increment: Every 2 seconds, the displayed number should increment by 1. The number should be displayed on the two 7-segment displays, with the tens digit on one display (sevseg1) and the units digit on the other (sevseg2).
LED Bar Graph: The LED bar graph (bargraph1) should light up a number of LEDs proportional to the displayed number. For example, if the number is 50, 5 LEDs should be lit.
Servo Motors: The two servo motors (servo1, servo2) should rotate to positions corresponding to the displayed number. The angle of each servo should be calculated as (number * 1.8) degrees, providing a range of 0 to 178.2 degrees.
Reset Condition: If the number exceeds 99, it should reset to 0, and all components should update accordingly.

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
    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    correct_num = cur_time // 2
    correct_sevseg1_value = sevseg_value[str(correct_num // 10)]
    correct_sevseg2_value = sevseg_value[str(correct_num % 10)]
    correct_servo1_value = correct_num * 1.8
    correct_servo2_value = correct_num * 1.8
    correct_bar1_value = [1 if i < correct_num // 10 else 0 for i in range(10)]
    # print(servo1_value, servo2_value, sevseg1_value, sevseg2_value, bar1_value)
    # print(correct_servo1_value, correct_servo2_value, correct_sevseg1_value, correct_sevseg2_value, correct_bar1_value)
    if abs(servo1_value - correct_servo1_value) < 1 and abs(servo2_value - correct_servo2_value) < 1 and np.allclose(sevseg1_value, correct_sevseg1_value, atol=deviation) and np.allclose(sevseg2_value, correct_sevseg2_value, atol=deviation) and np.allclose(bar1_value, correct_bar1_value, atol=deviation):
        return True
    else:
        return False


def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(8, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(14, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    
    # test 4
    correct_sleep(22, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    

    return res