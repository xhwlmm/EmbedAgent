'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 10-segment LED bar graph (bargraph1), two individual LEDs (led1, led2), and a push button (btn1). The bar graph will display a counter value that increases with each button press, while the LEDs will show how many times the counter has overflowed in binary format.

**Detail Rules**:
Initialization: All components must start in an off state (bar graph segments unlit, LEDs off).
Button Interaction:
1. Each valid button press increments the counter by 1.
2. The bar graph (bargraph1) must light up segments corresponding to the current counter value (1-10 segments,PIN A1-A10).
3. When the counter exceeds 10, it resets to 0 and the overflow counter (shown by LEDs) increments by 1.
4. The LEDs (led1, led2) display the overflow counter in binary:
   - 00: 0 overflows
   - 01: 1 overflow
   - 10: 2 overflows
   - 11: 3 overflows (then wraps back to 00)
5. Button presses must be debounced to prevent false triggers (minimum 0.15-second stable press detection).
6. The system must maintain each valid state (combination of bar graph segments and LED states) until the next valid button press.

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
    bar1 = get_bargraph_value(args['bargraph1'],driver)

    current = [led1,led2,*bar1]
    num = btn_click%44

    if num<=10:
        correct = [0,0] + [1]*(num%11) + [0]*(10-(num%11))
    elif num <=21:
        correct = [1,0] + [1]*(num%11) + [0]*(10-(num%11))
    elif num <=32:
        correct = [0,1] + [1]*(num%11) + [0]*(10-(num%11))
    elif num <=43:
        correct = [1,1] + [1]*(num%11) + [0]*(10-(num%11))
    else:
        return 0
    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_click = 0
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    for _ in range(5):
        click_button(args['btn1'], actions)
        btn_click += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    for _ in range(6):
        click_button(args['btn1'], actions)
        btn_click += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    for _ in range(9):
        click_button(args['btn1'], actions)
        btn_click += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)


    return res