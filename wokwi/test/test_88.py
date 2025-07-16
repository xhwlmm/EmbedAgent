'''

**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2), an RGB LED (rgb1), and two push buttons (btn1, btn2). The 7-segment displays will show a two-digit number, where one display represents the tens digit and the other represents the units digit. The RGB LED will change color based on the value of the displayed number. The push buttons will increment or decrement the displayed number by 1 each time they are pressed. If the number exceeds 99 or goes below 0, it should wrap around to the opposite limit.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00", and the RGB LED should be off.
Button Interaction:
1. Pressing the first button (btn1) increments the displayed number by 1. If the number exceeds 99, it wraps around to 0.
2. Pressing the second button (btn2) decrements the displayed number by 1. If the number goes below 0, it wraps around to 99.
RGB LED Behavior:
1. If the displayed number is between 0 and 33, the RGB LED should glow red.
2. If the displayed number is between 34 and 66, the RGB LED should glow green.
3. If the displayed number is between 67 and 99, the RGB LED should glow blue.
Display Update: The 7-segment displays and RGB LED should immediately update to reflect the new number and color after each button press.
Debouncing: Ensure that button presses are debounced to avoid false triggers caused by mechanical vibrations.

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



def test(clock, driver, args, seg_num, deviation=0.2):
    sevseg1_value = get_sevseg_value(args["sevseg1"],driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"],driver)
    rgb1_value = get_rgb_value(args["rgb1"],driver)

    current = [*sevseg1_value, *sevseg2_value, *rgb1_value]
    tens = seg_num // 10
    ones = seg_num % 10
    if 0<=seg_num<=33:
        correct = sevseg_value[str(tens)] + sevseg_value[str(ones)] + [1,0,0]
    elif 34<=seg_num<=66:
        correct = sevseg_value[str(tens)] + sevseg_value[str(ones)] + [0,1,0]
    elif 67<=seg_num<=99:
        correct = sevseg_value[str(tens)] + sevseg_value[str(ones)] + [0,0,1]
    else:
        return 0

    return np.allclose(current, correct, deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    time.sleep(1)
    seg_num = 0
    res["msg"].append(1 if test(clock, driver, args, seg_num) else 0)
    
    
    # test 2: click the button1
    click_button(args['btn2'], actions)
    seg_num = (seg_num + 100 - 1)%100
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, seg_num) else 0)


    # test 3: click the button2
    for _ in range(35):
        click_button(args['btn1'], actions)
        seg_num = (seg_num + 1)%100
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, seg_num) else 0)

    
    return res