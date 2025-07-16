'''

**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) using three slide potentiometers (pot1, pot2, pot3) and two push buttons (btn1, btn2). The RGB LED's color will be determined by the values of the potentiometers, and the push buttons will allow you to cycle through different color modes. The RGB LED should display the color corresponding to the current mode and potentiometer values.

**Detail Rules**:
Initialization: Upon powering on or resetting, the RGB LED (rgb1) should be off.
Potentiometer Interaction:
1. The first potentiometer (pot1) controls the intensity of the red component of the RGB LED.
2. The second potentiometer (pot2) controls the intensity of the green component of the RGB LED.
3. The third potentiometer (pot3) controls the intensity of the blue component of the RGB LED.
Button Interaction:
1. The first button (btn1) cycles through the following modes:
    - Mode 1: Only the red component is active.
    - Mode 2: Only the green component is active.
    - Mode 3: Only the blue component is active.
    - Mode 4: All three components (red, green, blue) are active.
2. The second button (btn2) resets the RGB LED to off and sets the mode back to Mode 1.
Display Update: The RGB LED should immediately update to reflect the current mode and potentiometer values after each button press or potentiometer adjustment.

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


def test(clock, driver, args, btn_num, click_num, pot_pos, deviation=0.2):
    rgb1_value = get_rgb_value(args["rgb1"],driver)

    color = [
        [1,0,0],
        [0,1,0],
        [0,0,1],
        [1,1,1]
    ]


    if btn_num == 1:
        correct = []
        for i in range(3):
            correct.append(pot_pos[i]*color[click_num%4][i])
    else:
        if pot_pos[0] == 1:
            correct = color[0]
        else:
            correct = [0,0,0]

    return np.allclose(rgb1_value, correct, deviation)

        

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init 
    time.sleep(1)
    bnt_num = 1
    click_num = 0
    pot_pos=[1,1,1]
    move_pot(args["pot1"],1,driver)
    move_pot(args["pot2"],1,driver)
    move_pot(args["pot3"],1,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, bnt_num, click_num, pot_pos) else 0)

 
    # test 2: click the button1 once 
    bnt_num = 1
    click_num = 1
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, bnt_num, click_num, pot_pos) else 0)


    # test 3: click the button1 twice
    bnt_num = 1
    click_num = 2
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    driver.save_screenshot('screenshot.png')

    res["msg"].append(1 if test(clock, driver, args, bnt_num, click_num, pot_pos) else 0)


    # test 4: click the button1 three times
    bnt_num = 1
    click_num = 3
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, bnt_num, click_num, pot_pos) else 0)


    # test 4: click the button2 
    bnt_num = 2
    click_num = 1
    click_button(args['btn2'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, bnt_num, click_num, pot_pos) else 0)

    return res