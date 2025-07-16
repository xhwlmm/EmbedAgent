'''

**Task**:
You are tasked with programming an Arduino (uno) to control two RGB LEDs (rgb1, rgb2), a 7-segment display (sevseg1), and three push buttons (btn1, btn2, btn3). The RGB LEDs will display specific colors based on the state of the buttons, and the 7-segment display will show a number corresponding to the number of times the buttons have been pressed. Each button press will increment the count, and the RGB LEDs will change colors based on the count's value.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should show "0", and both RGB LEDs should be off.
Button Interaction:
1. Each press of any button (btn1, btn2, btn3) should increment the count by 1. The count should be displayed on the 7-segment display. The range of the count is from 0 to 15. If the count exceeds 9, the 7-segment display should represent ones digits. If the count exceeds 15, it should reset to 0.
2. If the count is less than 5, RGB LED 1 (rgb1) should display red, and RGB LED 2 (rgb2) should display blue.
3. If the count is between 5 and 9, RGB LED 1 (rgb1) should display green, and RGB LED 2 (rgb2) should display yellow (a mix of red and green).
4. If the count is 10 or greater, RGB LED 1 (rgb1) should display purple (a mix of red and blue), and RGB LED 2 (rgb2) should display cyan (a mix of green and blue).
5. If the count exceeds 15, it should reset to 0, and the RGB LEDs should return to their initial state.
Display Update: The 7-segment display and RGB LEDs should immediately update to reflect the new count and color state after each button press.
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
from untils import sevseg_value,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,get_bargraph_value,click_button,get_servo_value


def test(clock, driver, args, click_num, deviation = 0.2):

    color = [
        [1,0,0,0,0,1],
        [0,1,0,1,1,0],
        [1,0,1,0,1,1]
    ]

    rgb1_value = get_rgb_value(args["rgb1"],driver)
    rgb2_value = get_rgb_value(args["rgb2"],driver)
    sevseg1_value = get_sevseg_value(args["sevseg1"],driver)


    current = [*rgb1_value, *rgb2_value, *sevseg1_value]

    if click_num < 5:
        correct = color[0] + sevseg_value[str(click_num)]
    elif click_num < 10 :
        correct = color[1] + sevseg_value[str(click_num)]
    elif click_num < 16:
        correct = color[2] + sevseg_value[str(click_num%10)]
    else:
        return 0

    return np.allclose(current, correct, deviation)



def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init 
    time.sleep(1)
    click_num = 0
    res["msg"].append(1 if test(clock, driver, args, click_num%16) else 0)

    # test 2: click the button1 
    colors = [1,0,0]
    for _ in range(6):
        click_button(args['btn1'], actions)
        click_num += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num%16) else 0)

    # test 3: click the button2 
    for _ in range(6):
        click_button(args['btn2'], actions)
        click_num += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num%16) else 0)

    # test 4: 
    for _ in range(4):
        click_button(args['btn3'], actions)
        click_num += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num%16) else 0)



    return res
