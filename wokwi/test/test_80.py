'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1), a push button (btn1), and a 10-segment LED bar graph (bargraph1). The 7-segment display will show a number between 0 and 9, and the LED bar graph will visually represent the same number by lighting up the corresponding number of LEDs. The push button will increment the displayed number by 1 each time it is pressed. If the number exceeds 9, it should reset to 0.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should show "0", and the LED bar graph should have no LEDs lit.
Button Interaction: Each press of the button (btn1) should increment the displayed number by 1. The number should be displayed on the 7-segment display (sevseg1), and the corresponding number of LEDs on the LED bar graph (bargraph1) should light up.
Reset Condition: If the number exceeds 9 after incrementing, both the 7-segment display and the LED bar graph should reset to "0" and no LEDs lit, respectively.
Display Update: The 7-segment display and the LED bar graph should immediately update to reflect the new number after each button press.

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

def test(clock, driver, args, click_num, deviation=0.2):
    sevseg1_value = get_sevseg_value(args["sevseg1"], driver)
    bargraph_value = get_bargraph_value(args["bargraph1"], driver)

    correct_sevseg1_value = sevseg_value[str(click_num%10)]
    correct_bargraph_value = [1]*(click_num%10)+[0]*(10-(click_num%10))

    current = [*sevseg1_value, *bargraph_value]
    correct = [*correct_sevseg1_value, *correct_bargraph_value]

    return np.allclose(current, correct, atol=deviation)


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: click the button1 once
    click_num = 1
    for _ in range(click_num):
        click_button(args['btn1'], actions)
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, 1) else 0)
    # test 2: click the button1 8 times
    click_num = 8
    for _ in range(click_num):
        click_button(args['btn1'], actions)
        time.sleep(0.5)

    res["msg"].append(1 if test(clock, driver, args, 9) else 0)

    # test 3: click the button1
    click_num = 1
    for _ in range(click_num):
        click_button(args['btn1'], actions)
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, 10) else 0)
    
    return res