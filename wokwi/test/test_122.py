'''

**Task**:
You are tasked with programming an Arduino (uno) to create a 3-bit binary input system using three push buttons (btn1, btn2, btn3), three LEDs (led1, led2, led3), and an 8-segment LED bar graph (bargraph1). The LED represents a single bit, and the bar graph displays the decimal equivalent of the binary value by illuminating a corresponding segment. The binary value is determined by three buttons (btn1, btn2, btn3).

**Detail Rules**:
1. **Initialization**: All LEDs and bar graph segments must be off when the system starts or resets.
2. **Button Interaction**:
    -Pressing btn1 will light up LED1, and the lowest bit of the binary number will switch to 1. Pressing btn1 again will switch the state of LED1 and the lowest bit of the binary number.
    -Pressing btn1 will light up LED2, and the middle bit of the binary number will switch to 1. Pressing btn2 again will switch the state of LED1 and the middle bit of the binary number.
    -Pressing btn1 will light up LED3, and the highest bit of the binary number will switch to 1. Pressing btn3 again will switch the state of LED1 and the highest bit of the binary number.
3. **Bar Graph Display**:
   - The bar graph lights up the segment corresponding to the 3-bit binary value (0-7).(PIN A1-A7) For example, binary `101` (decimal 5) lights segment 5.(PIN A5)
4. **State Stability**:
   - The system must ignore button presses shorter than 0.15 seconds to avoid false triggers.

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



def test(clock, driver, args, btn_click, deviation=0.2):

    led1 = get_led_value(args['led1'],driver)
    led2 = get_led_value(args['led2'],driver)
    led3 = get_led_value(args['led3'],driver)
    bar1 = get_bargraph_value(args['bargraph1'],driver)

    current = [led1,led2,led3,*bar1]
    num = btn_click[0]+2*btn_click[1]+4*btn_click[2]
    co_bar1 = [0,0,0,0,0,0,0,0,0,0]
    if num >0:
        co_bar1[num-1] = 1
    correct = [btn_click[0],btn_click[1],btn_click[2]] + co_bar1
    
    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_click = [0,0,0]
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    btn_click = [1,0,0]
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    btn_click = [1,1,0]
    click_button(args['btn2'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)


    btn_click = [1,1,1]
    click_button(args['btn3'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    return res