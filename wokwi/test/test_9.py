'''
**Task**:
You are tasked with programming an Arduino (uno) to control an LED bar graph (bargraph1) using a push button (btn1). The goal is to sequentially light up the LEDs in the bar graph from the bottom up, two at a time, each time the button is pressed. When all LEDs are lit, they should turn off and the sequence should restart from the bottom.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs in the LED bar graph should be off.
Button Interaction: Each press of the button (btn1) should light up the next two LEDs in the bar graph, starting from the bottom. The sequence should continue as follows:
First Press: The first two LEDs (from `A10` to `A0`) light up.
Second Press: The next two LEDs light up, making a total of four LEDs lit.
Third Press: The next two LEDs light up, making a total of six LEDs lit.
Fourth Press: The next two LEDs light up, making a total of eight LEDs lit.
Fifth Press: The next two LEDs light up, making all ten LEDs lit.
Sixth Press: All LEDs turn off, and the sequence restarts from the first two LEDs.
This sequence should repeat with each subsequent press of the button.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,sevseg_value,get_sevseg_value,get_bargraph_value,click_button

def test(driver, btn_cnt, args, deviation=0.2):
    bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
    status = np.array([*bargraph1_value])
    correct_num = (btn_cnt * 2) % 10
    correct = [1 if 10-i <= correct_num else 0 for i in range(10)]
    is_correct = np.allclose(status, correct, atol=deviation)
    return is_correct
        


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_cnt = 0
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)
    # test 2: click the button
    btn_cnt+=1
    click_button(args['btn1'], actions)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)

    # test 3: click the button twice
    btn_cnt+=1
    click_button(args['btn1'], actions)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)

    # test 4: click the button three times
    btn_cnt+=1
    click_button(args['btn1'], actions)
    res["msg"].append(1 if test(driver, btn_cnt, args) else 0)
    
    return res