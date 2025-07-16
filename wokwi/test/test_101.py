'''

**Task**:
You are tasked with programming an Arduino (uno) to control two LEDs (led1, led2) and a 7-segment display (sevseg1) using a shift register (sr1). The LEDs will blink alternately, and the 7-segment display will show a countdown from 9 to 0. The countdown should restart after reaching 0, and the LEDs should continue blinking throughout the process.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display (sevseg1) should show "9", and both LEDs (led1, led2) should be off.
LED Blinking: The LEDs should blink alternately with a 2-second interval. When one LED is on, the other should be off, and vice versa. The sequence should be led1 -> led2 -> led1 -> led2, and so on.
Countdown: The 7-segment display should decrement its displayed number every 4 seconds, starting from 9 and ending at 0.
Reset Condition: When the countdown reaches 0, the display should reset to 9, and the countdown should restart.
Display Update: The 7-segment display should update immediately to reflect the new number after each decrement.
LED Continuity: The LEDs should continue blinking alternately throughout the countdown process without interruption.

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



def test(clock, driver, args, deviation=0.2):
    led1_value = get_led_value(args['led1'],driver)
    led2_value = get_led_value(args['led2'],driver)
    sevseg1_value = get_sevseg_value(args['sevseg1'],driver)

    current = [led1_value, led2_value, *sevseg1_value]

    cur_time = get_clock(clock.text)

    cur_time = int(cur_time)

    cur_time = cur_time//2

    correct = [(cur_time+1)%2,cur_time%2, *sevseg_value[str(9-(cur_time%20)//2)]]

    return np.allclose(current, correct, deviation)
        
          
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(2.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(6.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(10.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(14.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res