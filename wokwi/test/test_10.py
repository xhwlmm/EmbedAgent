'''
**Task**:
You are tasked with programming an Arduino (uno) to control an LED bar graph (bargraph1) using a slide potentiometer (pot1) and a pushbutton (btn1). The number of LEDs lit on the bar graph should change based on the value of the potentiometer. Additionally, pressing the button should reverse the order in which the LEDs are lit.

**Detail Rules**:
Initialization: Upon powering on or resetting, the LED bar graph should be off.
Potentiometer Interaction: As the value of the potentiometer increases, the number of LEDs lit on the bar graph should increase, starting from the first LED (with pin: A10).
Button Interaction: When the button is pressed, the order in which the LEDs are lit should reverse. Specifically, the LEDs should start lighting from the last LED (with pin: A1) instead of the first.
State After Each Step:
1. When the potentiometer value increases, more LEDs should light up starting from the first LED.
2. When the potentiometer value decreases, fewer LEDs should remain lit, starting from the first LED.
3. When the button is pressed, the order of lighting the LEDs should reverse, and the number of LEDs lit should still correspond to the potentiometer value.
4. When the button is pressed again, the order of lighting the LEDs should return to the original sequence.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,sevseg_value,get_sevseg_value,move_pot,click_button,get_bargraph_value

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
    status = np.array([*bargraph1_value])
    correct = np.array([0 for i in range(10)])
    if np.allclose(status, correct, 0.2):
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    
    # test 2: move port to 0.5
    move_pot(args['pot1'], 0.2, driver)
    time.sleep(1)
    bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
    if bargraph1_value[0] == 0:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 3: click button
    click_button(args['btn1'],actions)
    time.sleep(1)
    raw_bargraph1_value = bargraph1_value
    bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
    if bargraph1_value[-1] == 0:
        res['msg'].append(1)
    else:
        res['msg'].append(0)

    # test 4: move port to 1
    move_pot(args['pot1'], 1, driver)
    time.sleep(1)
    bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
    correct = np.array([1 for i in range(10)])
    if np.allclose(bargraph1_value, correct, 0.2):
        res['msg'].append(1)
    else:
        res['msg'].append(0)

    return res