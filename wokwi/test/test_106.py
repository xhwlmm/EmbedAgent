'''

**Task**:
Program the Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2), a 10-segment LED bar graph (bargraph1), and two LEDs (led1, led2) using shift registers (sr1, sr2). The system displays an incrementing number from 00 to 99, visualizes its magnitude on the bar graph, and blinks the LEDs alternately every 2 seconds.

**Detail Rules**:
1. **Initialization**: 
   - 7-segment displays show "00".
   - LED bar graph (bargraph1) lights up 1 segment.(PIN A1)
   - Both LEDs (led1, led2) remain off.

2. **Increment Cycle**:
   - The displayed number increases by 1 every 2 seconds. After reaching 99, it resets to 00.
   - The 7-segment displays update to show the tens digit on sevseg1 and the units digit on sevseg2.

3. **Bar Graph Behavior**:
   - The bar graph lights up a number of segments equal to the tens digit + 1 (e.g., 25 → 3 segments, 90 → 10 segments).(PIN A1-A10)

4. **LED Blinking**:
   - led1 and led2 alternate states every 2 seconds (e.g., led1 on/led2 off for 2 seconds, then led1 off/led2 on).

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
from untils import sevseg_value,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,get_bargraph_value,click_button,get_servo_value,correct_sleep



def test(clock, driver, args, deviation=0.2):
    sevseg1_value = get_sevseg_value(args["sevseg1"],driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"],driver)
    bar1_value = get_bargraph_value(args["bargraph1"],driver)
    led1_value = get_led_value(args['led1'],driver)
    led2_value = get_led_value(args['led2'],driver)

    current = [led1_value,led2_value,*bar1_value,*sevseg1_value,*sevseg2_value]

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    num = (cur_time//2)%100
    tens = num//10
    ones = num%10
    if num == 0:
        co_led = [0,0]
    else:
        co_led = [num%2,(num+1)%2]

    correct = co_led + [1]*(tens+1) + [0]*(9-tens) + sevseg_value[str(tens)] + sevseg_value[str(ones)]


    return np.allclose(current, correct, deviation)




def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(2.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(4.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(6.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(10.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(12.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res