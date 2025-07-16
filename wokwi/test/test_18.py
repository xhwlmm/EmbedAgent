'''
**Task**:
You are tasked with programming an Arduino (uno) to control three RGB LEDs (rgb1, rgb2, rgb3) in a specific sequence. The LEDs should cycle through a predefined pattern of colors, with each color being displayed for 2 seconds.

**Detail Rules**:
Initialization: Upon powering on or resetting, all RGB LEDs should be off.
LED Sequence: The LEDs should cycle through the following color patterns in order, with each pattern lasting for 2 seconds:
1. First Pattern: 
   - LED1 (rgb1) displays red.
   - LED2 (rgb2) displays blue.
   - LED3 (rgb3) displays green.
2. Second Pattern: 
   - LED1 (rgb1) displays green.
   - LED2 (rgb2) displays red.
   - LED3 (rgb3) displays blue.
3. Third Pattern: 
   - LED1 (rgb1) displays blue.
   - LED2 (rgb2) displays green.
   - LED3 (rgb3) displays red.
This sequence should repeat indefinitely after the third pattern.
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
import time
import sys
import os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from untils import wait_for_element,move_pot,get_rgb_value,get_clock

def judge_color(clock, rgb1, rgb2, rgb3, driver, deviation = 0.2):

    rgb_color = [[(1,0,0),(0,0,1),(0,1,0)],[(0,1,0),(1,0,0),(0,0,1)],[(0,0,1),(0,1,0),(1,0,0)]]

    rgb1_color = get_rgb_value(rgb1, driver)
    rgb2_color = get_rgb_value(rgb2, driver)
    rgb3_color = get_rgb_value(rgb3, driver)
    current = [rgb1_color,rgb2_color,rgb3_color]
    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    correct = rgb_color[(cur_time//2)%3]

    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    # test 1: in 1s, red, blue, green
    time.sleep(1)
    if judge_color(clock, args['rgb1'], args['rgb2'], args['rgb3'], driver):
        res["msg"].append(1)
    else:
        res["msg"].append(0)

    # test 2: in 3s, green, red, blue
    time.sleep(1.7)
    if judge_color(clock, args['rgb1'], args['rgb2'], args['rgb3'], driver):
        res["msg"].append(1)
    else:
        res["msg"].append(0)

    # test 3: in 5s, blue, green, red
    time.sleep(1.7)
    if judge_color(clock, args['rgb1'], args['rgb2'], args['rgb3'], driver):
        res["msg"].append(1)
    else:
        res["msg"].append(0)
    

    return res