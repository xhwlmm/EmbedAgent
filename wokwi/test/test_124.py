'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) using a shift register (sr1), two push buttons (btn1, btn2), and an LED (led1). The 7-segment display will show a single-digit number that can be incremented or decremented using the push buttons. The LED will indicate whether the number is even or odd. 

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should show "0", and the LED (led1) should be off.
Button Interaction:
1. The first push button (btn1) increments the displayed number by 1. If the number exceeds 9, it should reset to 0.
2. The second push button (btn2) decrements the displayed number by 1. If the number goes below 0, it should reset to 9.
LED State:
1. If the displayed number is even, the LED (led1) should turn on.
2. If the displayed number is odd, the LED (led1) should turn off.
Display Update: The 7-segment display and LED should immediately update to reflect the new number and its parity after each button press.
Debouncing: Ensure that each button press is debounced to avoid false triggers caused by mechanical vibrations.

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

    sevseg1 = get_sevseg_value(args['sevseg1'],driver)

    current = [led1,*sevseg1]
    num = btn_click[0]-btn_click[1]
    if num%2 == 0:
        correct = [1,*sevseg_value[str(num%10)]]
    else:
        correct = [0,*sevseg_value[str(num%10)]]

    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_click = [0,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    for _ in range(3):
        click_button(args['btn1'], actions)
        btn_click[0] += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    for _ in range(3):
        click_button(args['btn2'], actions)
        btn_click[1] += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    return res