'''

**Task**:
You are tasked with programming an Arduino (uno) to control two LEDs (led1, led2) using three push buttons (btn1, btn2, btn3). The LEDs will act as indicators for specific button interactions. The first button (btn1) will toggle the state of the first LED (led1), the second button (btn2) will toggle the state of the second LED (led2), and the third button (btn3) will reset both LEDs to their off state.

**Detail Rules**:
Initialization: Upon powering on or resetting, both LEDs (led1, led2) should be off.
Button Interactions:
1. Pressing the first button (btn1) should toggle the state of the first LED (led1). If the LED is off, it should turn on, and vice versa. The state should remain stable for 2 seconds after each toggle.
2. Pressing the second button (btn2) should toggle the state of the second LED (led2). If the LED is off, it should turn on, and vice versa. The state should remain stable for 2 seconds after each toggle.
3. Pressing the third button (btn3) should reset both LEDs (led1, led2) to their off state, regardless of their current state. The off state should remain stable for 2 seconds after the reset.
Debouncing: Each button press should be debounced to avoid false triggers caused by mechanical vibrations.

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



def test(clock, driver, args, btn_click, last_click, deviation=0.2):

    led1 = get_led_value(args['led1'],driver)
    led2 = get_led_value(args['led2'],driver)


    current = [led1,led2]
    if last_click == 3:
        correct = [0,0]
    else:
        correct = [btn_click[0]%2,btn_click[1]%2]

    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_click = [0,0,0]
    last_click = 0
    res["msg"].append(1 if test(clock, driver, args, btn_click, last_click) else 0)

    btn_click = [1,0,0]
    last_click = 1
    click_button(args['btn1'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click, last_click) else 0)

    btn_click = [1,1,0]
    last_click = 2
    click_button(args['btn2'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click, last_click) else 0)

    btn_click = [2,1,0]
    last_click = 1
    click_button(args['btn1'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click, last_click) else 0)

    btn_click = [2,1,1]
    last_click = 3
    click_button(args['btn3'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click, last_click) else 0)

    return res