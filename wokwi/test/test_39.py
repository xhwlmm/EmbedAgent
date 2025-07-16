'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) and a 10-segment LED bar graph (bargraph1) using a shift register (sr1). The 7-segment display will show a single digit, and the LED bar graph will visually represent the same number by lighting up a corresponding number of LEDs. The number displayed should increment every 2 seconds, and when it reaches 9, it should reset to 0.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display (sevseg1) should show "0", and the LED bar graph (bargraph1) should have no LEDs lit.
Incrementing: Every 2 seconds, the number displayed on the 7-segment display (sevseg1) should increment by 1. Simultaneously, the LED bar graph (bargraph1) should light up a number of LEDs equal to the current number (from pin A1 to A10).
Reset Condition: When the number reaches 9, it should reset to 0, and the LED bar graph (bargraph1) should turn off all LEDs.
Display Update: The 7-segment display (sevseg1) and the LED bar graph (bargraph1) should update immediately to reflect the new number.

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
    bar1_value = get_bargraph_value(args["bargraph1"], driver)
    sevseg1_value = get_sevseg_value(args["sevseg1"], driver)
    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    correct_num = cur_time // 2
    correct_num = correct_num % 10
    correct_bar1_value = [0 for i in range(10)]
    for i in range(correct_num):
        correct_bar1_value[i] = 1
    correct_sevseg1_value = sevseg_value[str(correct_num)]
    if np.allclose(correct_sevseg1_value, sevseg1_value, atol=deviation) and np.allclose(bar1_value, correct_bar1_value, atol=deviation):
        return True
    else:
        return False


def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(8.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(16.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    
    # test 4
    correct_sleep(24.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    

    return res