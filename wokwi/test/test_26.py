'''

**Task**:
You are tasked with programming an Arduino (uno) to control two LED bar graphs (bargraph1, bargraph2). The LED bar graphs will display a pattern where the LEDs light up sequentially from left to right and then from right to left, creating a "knight rider" effect. Both bar graphs should synchronize their patterns.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs in both bar graphs (bargraph1, bargraph2) should be off.
Pattern Execution:
1. The LEDs in both bar graphs should light up sequentially from left to right. For bargrapth1, it should start with LED 1 and proceed to LED 10 (pin:A1 to pin:A10). when bargraph1 reaches LED i, bargraph2 should reach with LED i-1. If bargraph1 reaches LED 1, bargraph2 should turn off.
2. After reaching the rightmost LED (LED 10), the LEDs should light up sequentially from right to left (LED 10 to LED 1) with the same delay.For bargrapth1, it should start with LED 10 and proceed to LED 1 (pin:A10 to pin:A1). when bargraph1 reaches LED i, bargraph2 should reach with LED i-1. If bargraph1 reaches LED 1, bargraph2 should turn off. The time delay between each LED lighting up should be 2 seconds.
3. This pattern should repeat indefinitely.
Synchronization: Both bar graphs (bargraph1, bargraph2) must display the same pattern simultaneously.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,correct_sleep

def test(clock, driver, args, deviation=0.2):

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)

    bargraph1_value = get_bargraph_value(args["bargraph1"], driver)
    bargraph2_value = get_bargraph_value(args["bargraph2"], driver)

    if (cur_time // 20) % 2 == 0:
        correct_index = (cur_time % 20) // 2
    else:
        correct_index = 9 - (cur_time % 20) // 2
    correct_bar1 = [0] * 10
    correct_bar2 = [0] * 10
    correct_bar1[correct_index] = 1

    if correct_index != 0:
        correct_bar2[correct_index-1] = 1

    return np.allclose(np.array(bargraph1_value), np.array(correct_bar1), rtol=deviation) and np.allclose(np.array(bargraph2_value), np.array(correct_bar2), rtol=deviation)
        


def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(1.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    
    # test 4
    correct_sleep(13,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 5
    correct_sleep(23,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    

    return res