'''
**Task**:
You are tasked with programming an Arduino (uno) to control three LEDs (led_red, led_yellow, led_green) and a 7-segment display (sevseg1) using a shift register (sr1). The goal is to randomly light up 0 to 3 LEDs every 2 seconds and display the number of currently lit LEDs on the 7-segment display.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs should be off, and the 7-segment display should show '0'.
Randomization: Every 2 seconds, the system should randomly select 0 to 3 LEDs to light up. The selection of which LEDs to light should be random each time.
Display Update: The 7-segment display should immediately update to show the number of LEDs that are currently lit.
Cycle Continuation: This process should repeat indefinitely, with the LEDs and 7-segment display updating every 2 seconds.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,correct_sleep

def test(driver, clock, args, deviation=0.2):
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    led1_value = get_led_value(args['led_red'], driver) > 0.5
    led2_value = get_led_value(args['led_yellow'], driver) > 0.5
    led3_value = get_led_value(args['led_green'], driver) > 0.5
    status = np.array([*sevseg1_value])
    correct = led1_value + led2_value + led3_value
    correct = str(correct)
    correct = np.array([*sevseg_value[correct[0]]])
    is_correct = np.allclose(status, correct, atol=deviation)
    return is_correct
        


def test_func(driver, clock, args, res):
    # test 1: 1s
    correct_sleep(0.5,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 2: 3s
    correct_sleep(2.5,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 3: 6s
    correct_sleep(6.5,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    
    return res