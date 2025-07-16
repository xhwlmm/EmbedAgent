'''

**Task**:
You are tasked with programming an Arduino (uno) to create an interactive color and level indicator using two RGB LEDs (rgb1, rgb2), a push button (btn1), and a 7-segment LED bar graph (bargraph1). The system will cycle through predefined modes where each mode changes the colors of the RGB LEDs and activates a specific number of LEDs in the bar graph.

**Detail Rules**:
1. **Initialization**:  
   - All components start in an OFF state when powered on or reset.  
   - The LED bar graph (bargraph1) shows no lit LEDs.  
   - Both RGB LEDs (rgb1, rgb2) remain off.  

2. **Button Interaction**:  
   - Each valid press of the button (btn1) increments the system mode by 1.  
   - A valid press is defined as holding the button for **at least 0.15 seconds** to avoid false triggers.  
   - After 7 presses (reaching mode 7), the next press resets the mode to 0.  

3. **Mode Behavior**:  
   - **Mode 0**: All components are OFF.  
   - **Modes 1-7**:  
     - The RGB LEDs (rgb1, rgb2) display unique color combinations (e.g., red/blue, green/cyan) for each mode.  
     - The LED bar graph (bargraph1) lights up a number of LEDs equal to the current mode (e.g., 3 LEDs for mode 3).(The pins of the bar chart are A1-A7)

4. **Color Rules**:  
   - Both RGB LEDs must change colors synchronously with each mode transition.  
   - The order of colors in the RGB LEDs should follow the folling sequence: (red/blue, green/cyan, yellow/magenta, cyan/yellow, meagenta/cyan, white/yellow, black/white).

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


def test(clock, driver, args, btn_num, deviation = 0.2):
    rgb1_value = get_rgb_value(args["rgb1"],driver)
    rgb2_value = get_rgb_value(args["rgb2"],driver)

    color = [
        [0,0,0,0,0,0],
        [1,0,0,0,0,1],
        [0,1,0,0,1,1],
        [1,1,0,1,0,1],
        [0,1,1,1,1,0],
        [1,0,1,0,1,1],
        [1,1,1,1,1,0],
        [0,0,0,1,1,1]
    ]
    bar1_value = get_bargraph_value(args['bargraph1'],driver)
    current = [*rgb1_value, *rgb2_value, *bar1_value]
    correct = color[btn_num%8] + [1]*(btn_num%8) + [0]*(10-btn_num%8)

    return np.allclose(current, correct, deviation)



def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init 
    time.sleep(1)
    bnt_num = 0
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, bnt_num) else 0)

    # test 2: click the button1 
    for _ in range(3):
        click_button(args['btn1'], actions)
        bnt_num += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, bnt_num) else 0)

    # test 3: click the button2 
    for _ in range(2):
        click_button(args['btn1'], actions)
        bnt_num += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, bnt_num) else 0)

    # test 4: 
    for _ in range(2):
        click_button(args['btn1'], actions)
        bnt_num += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, bnt_num) else 0)

    click_button(args['btn1'], actions)
    bnt_num += 1
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, bnt_num) else 0)

    return res