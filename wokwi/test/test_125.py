'''

**Task**:
You are tasked with programming an Arduino (uno) to control three single-color LEDs (led1, led2, led3) and three RGB LEDs (rgb1, rgb2, rgb3) using a push button (btn1). The single-color LEDs will act as indicators for the state of the RGB LEDs, and the push button will cycle through different lighting modes for the RGB LEDs. Each mode will display a unique color combination on the RGB LEDs, and the single-color LEDs will indicate the current mode.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs (single-color and RGB) should be off.
Button Interaction:
1. Each press of the button (btn1) will cycle through four modes:
   - Mode 1: RGB LEDs display red, green, and blue colors respectively. led1 will turn on in sequence to indicate the mode.
   - Mode 2: RGB LEDs display a rainbow effect (yellow, cyan, purple)
   - Mode 3: RGB LEDs display a warm white color (equal red, green, and blue values). led3 will turn on in sequence to indicate the mode.
   - Mode 4: All LEDs (single-color and RGB) turn off. Single-color LEDs will remain off to indicate the mode.
2. Each mode should be maintained for at least 2 seconds before the button can cycle to the next mode.
3. The RGB LEDs should smoothly transition between colors in Mode 2 (rainbow effect).
4. The single-color LEDs should clearly indicate the current mode as described above.

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

    rgb1 = get_rgb_value(args['rgb1'],driver)
    rgb2 = get_rgb_value(args['rgb2'],driver)
    rgb3 = get_rgb_value(args['rgb3'],driver)

    current = [led1,led2,led3,*rgb1,*rgb2,*rgb3]

    if btn_click%4 == 0:
        correct = [1,0,0,1,0,0,0,1,0,0,0,1]
    elif btn_click%4 == 1:
        correct = [0,1,0,1,1,0,0,1,1,1,0,1]
    elif btn_click%4 == 2:
        correct = [0,0,1,1,1,1,1,1,1,1,1,1]
    elif btn_click%4 == 3:
        correct = [0,0,0,0,0,0,0,0,0,0,0,0]
    else:
        return 0

    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_click = 0
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    btn_click = 1
    click_button(args['btn1'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    btn_click = 2
    click_button(args['btn1'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    btn_click = 3
    click_button(args['btn1'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    btn_click = 4
    click_button(args['btn1'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    return res