'''
**Task**:
You are tasked with programming an Arduino (uno) to control an LED bar graph (bargraph1). The goal is to create a sequence where the LEDs on the bar graph alternate between even and odd positions.

**Detail Rules**:
Initialization: Upon powering on or resetting, the LED bar graph should have all LEDs in the even positions lit (A0 A2 ....).
Sequence: After 2 seconds, the LEDs in the even positions should turn off, and the LEDs in the odd positions should turn on.
Alternation: This sequence should continue indefinitely, with the LEDs alternating between even and odd positions every 2 seconds.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_bargraph_value,get_clock, correct_sleep

def test(driver, clock, args, deviation=0.2):
    bargraph1_value = get_bargraph_value(args["bargraph1"], driver)
    status = np.array([*bargraph1_value])
    correct = 0
    cur_time = get_clock(clock.text)
    correct_lst = [[0,1,0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0,1,0]]
    correct = correct_lst[(int(cur_time)//2)%2]
    correct = np.array(correct)
    is_correct = np.allclose(status, correct, atol=deviation)
    return is_correct
        


def test_func(driver, clock, args, res):
    # test 1: 1s
    correct_sleep(0.5,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 2: 3s
    correct_sleep(2.5,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    # test 3: 5s
    correct_sleep(4.5,clock)
    res["msg"].append(1 if test(driver, clock, args) else 0)
    
    return res