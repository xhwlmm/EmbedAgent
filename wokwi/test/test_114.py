'''

**Task**:
You are tasked with programming an Arduino (uno) to control two single-color LEDs (led1, led2), two RGB LEDs (rgb1, rgb2), and a 6-segment LED bar graph (bargraph1). The system must cycle through three distinct lighting patterns, each lasting 2 seconds, using all components in every state.

**Detail Rules**:
1. **Initialization**: All LEDs and bar graph segments must be off when the system starts or resets.
2. **State 1 (Duration: 2 seconds)**:
   - The monochrome LED (led1) lights up and the monochrome LED (led2) goes out.
   - RGB LED (rgb1) displays red.
   - The first three segments of the bar graph (bargraph1) light up.(PIN A1-A3)
3. **State 2 (Duration: 2 seconds)**:
   - The monochrome LED (led2) lights up and the monochrome LED (led1) goes out.
   - RGB LED (rgb2) displays green.
   - The last three segments of the bar graph (bargraph1) light up.(PIN A4-A6)
4. **State 3 (Duration: 2 seconds)**:
   - Both monochrome LEDs (LED 1, LED 2) are lit up.
   - Both RGB LEDs (rgb1, rgb2) display a cyan color (blue + green).
   - All six segments of the bar graph (bargraph1) light up.(PIN A1-A6)
5. **Cycle**: Repeat states 1-3 indefinitely.

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



def test(clock, driver, args,deviation=0.2):

    led1 = get_led_value(args['led1'],driver)
    led2 = get_led_value(args['led2'],driver)
    rgb1_value = get_rgb_value(args["rgb1"],driver)
    rgb2_value = get_rgb_value(args["rgb2"],driver)
    bar1_value = get_bargraph_value(args["bargraph1"],driver)

    current = [led1,led2,*rgb1_value,*rgb2_value,*bar1_value]

    cur_time = get_clock(clock.text)

    cur_time = int(cur_time)
    if (cur_time//2)%3 == 0:
        correct = [1,0,1,0,0,0,0,0] + [1,1,1,0,0,0,0,0,0,0]
    elif (cur_time//2)%3 == 1:
        correct = [0,1,0,0,0,0,1,0] + [0,0,0,1,1,1,0,0,0,0]
    else:
        correct = [1,1,0,1,1,0,1,1] + [1,1,1,1,1,1,0,0,0,0]

    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(2.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(6.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(10.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(14.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res