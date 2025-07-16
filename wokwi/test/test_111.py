'''

**Task**:
You are tasked with programming an Arduino (uno) to control three single-color LEDs (led1, led2, led3) and an RGB LED (rgb1) using a slide potentiometer (pot1). The potentiometer will determine the brightness of the RGB LED and the state of the single-color LEDs. The single-color LEDs will act as indicators for different brightness ranges of the RGB LED.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs (led1, led2, led3, rgb1) should be off.
Potentiometer Interaction:
1. The slide potentiometer (pot1) will control the brightness of the RGB LED (rgb1). The value of the potentiometer is mapped to a brightness level between 0 and 255 for each color channel (R, G, B).
2. The single-color LEDs (led1, led2, led3) will act as indicators for the brightness level of the RGB LED:
   - If the potentiometer value is in the lower third (0-341), only led1 should be on.
   - If the potentiometer value is in the middle third (342-682), only led2 should be on.
   - If the potentiometer value is in the upper third (683-1023), only led3 should be on.
3. The RGB LED (rgb1) should display a color based on the potentiometer value:
   - The red channel should be at maximum brightness when the potentiometer is in the lower third.
   - The green channel should be at maximum brightness when the potentiometer is in the middle third.
   - The blue channel should be at maximum brightness when the potentiometer is in the upper third.
4. The state of the LEDs should update continuously based on the potentiometer value.

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


def test(clock, driver, args, pot_pos, deviation=0.2):
    rgb1 = get_rgb_value(args['rgb1'],driver)

    led1 = get_led_value(args["led1"],driver)
    led2 = get_led_value(args["led2"],driver)
    led3 = get_led_value(args["led3"],driver)


    current = [led1,led2,led3,*rgb1]

    if pot_pos == 1:
        correct = [0,0,1,0,0,1] 
    elif pot_pos == 0:
        correct = [1,0,0,1,0,0]
    else:
        return 0

    return np.allclose(current, correct, deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    pot_pos = 0
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    # test 2
    pot_pos = 1
    move_pot(args["pot1"],1,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    # test 3
    pot_pos = 0
    move_pot(args["pot1"],0,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    
    return res