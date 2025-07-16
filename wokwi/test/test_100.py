'''

**Task**:
You are tasked with programming an Arduino (uno) to control two individual LEDs (led1, led2) and a 10-segment LED bar graph (bargraph1) using three slide potentiometers (pot1, pot2, pot3). The potentiometers will control the brightness of the individual LEDs and the number of illuminated segments on the LED bar graph.

**Detail Rules**:
Initialization: Upon powering on or resetting, both individual LEDs (led1, led2) and all segments of the LED bar graph (bargraph1) should be off.
Potentiometer Interaction:
1. The first potentiometer (pot1) controls the brightness of the first LED (led1). The value of pot1 is mapped uniformly from 0 to 255.
2. The second potentiometer (pot2) controls the brightness of the second LED (led2). The value of pot2 is mapped uniformly from 0 to 255.
3. The third potentiometer (pot3) controls the number of illuminated segments(PIN A1-A10) on the LED bar graph (bargraph1). The value of pot3 is mapped uniformly from 0 to 10, where 0 means no segments are lit, and 10 means all segments are lit.
The brightness of the individual LEDs and the number of illuminated segments on the LED bar graph should be updated continuously based on the current values of the potentiometers.

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



def test(clock, driver, args, pot_pos, deviation=0.2):
    led1_value = get_led_value(args["led1"],driver)
    led2_value = get_led_value(args["led2"],driver)
    bargraph1_value = get_bargraph_value(args["bargraph1"],driver)

    current = [led1_value, led2_value, *bargraph1_value]
    correct = [pot_pos[0], pot_pos[1]] + [pot_pos[2]] *10

    return np.allclose(current, correct, deviation)
        
          
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    time.sleep(1)
    pot_pos = [0,0,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)

    # test 2
    pot_pos = [1,0,0]
    move_pot(args["pot1"],1,driver)
    move_pot(args["pot2"],0,driver)
    move_pot(args["pot3"],0,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)

    # test 3
    pot_pos = [1,1,0]
    move_pot(args["pot1"],1,driver)
    move_pot(args["pot2"],1,driver)
    move_pot(args["pot3"],0,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)

    # test 4
    pot_pos = [1,1,1]
    move_pot(args["pot1"],1,driver)
    move_pot(args["pot2"],1,driver)
    move_pot(args["pot3"],1,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)

    return res