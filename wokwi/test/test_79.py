'''

**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2). The displays will show a two-digit number that can be incremented or decremented using three push buttons (btn1, btn2, btn3). Additionally, a slide potentiometer (pot1) will control the speed at which the number changes when a button is held down. The number should wrap around to 0 if it exceeds 99 or to 99 if it goes below 0.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00".
Button Interaction:
1. The first button (btn1) increments the displayed number by 1 each time it is pressed.
2. The second button (btn2) decrements the displayed number by 1 each time it is pressed.
3. The third button (btn3) resets the displayed number to 0 when pressed.
Speed Control: The slide potentiometer (pot1) controls the speed of incrementing or decrementing when a button is held down. The speed should range from 0.1 seconds to 1 second per step, based on the potentiometer's value.
Display Update: The 7-segment displays should immediately update to reflect the new number after each button press or hold.
Wrap-around: If the number exceeds 99, it should reset to 0. If the number goes below 0, it should reset to 99.

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
from untils import sevseg_value,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,get_bargraph_value,click_button,get_servo_value

def get_number(args,driver):
    def get_key (dict, value):
        for k, v in dict.items():
            if v == value:
                return int(k)
    sevseg1 = [(1 if i>=0.5 else 0) for i in get_sevseg_value(args,driver)]
    return get_key (sevseg_value, sevseg1)

def test(clock, driver, args, seg_num):
    sevseg1_value = get_number(args["sevseg1"],driver)
    sevseg2_value = get_number(args["sevseg2"],driver)
    num = sevseg1_value*10 + sevseg2_value
    return 0<=num<=99 and num == seg_num

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: click the button1
    click_button(args['btn1'], actions, consist_time = 2.05)
    time.sleep(0.5)
    seg_num = 21
    res["msg"].append(1 if test(clock, driver, args, seg_num) else 0)

    # test 2: click the button2
    click_button(args['btn2'], actions, consist_time = 2.05)
    time.sleep(0.5)
    seg_num = 0
    res["msg"].append(1 if test(clock, driver, args, seg_num) else 0)

    # test 3: change the pot1, click button1
    move_pot(args["pot1"], 1, driver)
    time.sleep(0.5)
    click_button(args['btn1'], actions, consist_time = 2.1)
    time.sleep(2)
    seg_num = 3
    res["msg"].append(1 if test(clock, driver, args, seg_num) else 0)

    # test 4: click button3
    click_button(args['btn3'], actions, consist_time = 2.1)
    time.sleep(0.5)
    seg_num = 0
    res["msg"].append(1 if test(clock, driver, args, seg_num) else 0)

    # test 5: change the pot2, click button2
    click_button(args['btn2'], actions, consist_time = 2.1)
    time.sleep(0.5)
    seg_num = 97
    res["msg"].append(1 if test(clock, driver, args, seg_num) else 0)

    
    return res