'''

**Task**:
You are tasked with programming an Arduino (uno) to control a system consisting of three single-color LEDs (led1, led2, led3), two RGB LEDs (rgb1, rgb2), and two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2). The system should display a countdown from 9 to 0 on the 7-segment displays, with the LEDs and RGB LEDs providing visual feedback during the countdown.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "99", and all LEDs and RGB LEDs should be off.
Countdown Sequence:
1. The countdown starts at 9 and decrements by 1 every 2 seconds.
2. The 7-segment displays should update to reflect the current countdown value, if the value is 8, 7-segment displays should show "88".
3. During the countdown:
   - The single-color LEDs (led1, led2, led3) should light up in sequence (led1, then led2, then led3) for each countdown step, with each LED staying on for 2 seconds.
   - The RGB LEDs (rgb1, rgb2) should cycle through the colors red, green, and blue, changing color every 2 seconds.
4. When the countdown reaches 0, the 7-segment displays should show "00", all single-color LEDs should turn off, and the RGB LEDs should display a steady white light.
5. The system should then reset and restart the countdown from 9.

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



def test(clock, driver, args,deviation=0.2):

    led1 = get_led_value(args['led1'],driver)
    led2 = get_led_value(args['led2'],driver)
    led3 = get_led_value(args['led3'],driver)

    rgb1_value = get_rgb_value(args["rgb1"],driver)
    rgb2_value = get_rgb_value(args["rgb2"],driver)
    sevseg1_value = get_sevseg_value(args["sevseg1"],driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"],driver)

    current = [led1,led2,led3,*rgb1_value,*rgb2_value,*sevseg1_value,*sevseg2_value]

    cur_time = get_clock(clock.text)

    cur_time = int(cur_time)

    if (cur_time//2)%10 == 9:
        correct = [0,0,0,1,1,1,1,1,1,*sevseg_value['0'],*sevseg_value['0']]
    else:
        if (cur_time//2)%3 == 0:
            correct = [1,0,0,1,0,0,1,0,0,*sevseg_value[str(9-(cur_time//2)%10)],*sevseg_value[str(9-(cur_time//2)%10)]]
        elif (cur_time//2)%3 == 1:
            correct = [0,1,0,0,1,0,0,1,0,*sevseg_value[str(9-(cur_time//2)%10)],*sevseg_value[str(9-(cur_time//2)%10)]]
        else:
            correct = [0,0,1,0,0,1,0,0,1,*sevseg_value[str(9-(cur_time//2)%10)],*sevseg_value[str(9-(cur_time//2)%10)]]


    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(0.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(2.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(4.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(6.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res