'''

**Task**:
You are tasked with programming an Arduino (uno) to control the brightness of an LED (led1) using two slide potentiometers (pot1, pot2). The first potentiometer (pot1) will control the brightness of the LED, while the second potentiometer (pot2) will act as a threshold. If the brightness value from pot1 exceeds the threshold value from pot2, the LED should turn on at the brightness level set by pot1. Otherwise, the LED should remain off.

**Detail Rules**:
Initialization: Upon powering on or resetting, the LED (led1) should be off.
Potentiometer Interaction:
1. The first potentiometer (pot1) determines the brightness of the LED. Its value ranges from 0 to 1023, which should be mapped to a brightness level between 0 and 255.
2. The second potentiometer (pot2) sets a threshold value. Its value also ranges from 0 to 1023.
3. If the brightness value from pot1 exceeds the threshold value from pot2, the LED should turn on at the brightness level set by pot1.
4. If the brightness value from pot1 is less than or equal to the threshold value from pot2, the LED should remain off.
5. The LED's state and brightness should be updated continuously based on the current values of the potentiometers.

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



def test(clock, driver, args, pot1_value, pot2_value, deviation=0.2):
    led1_value = get_led_value(args["led1"],driver)

    if pot1_value > pot2_value:
        return np.allclose(1,led1_value,deviation)
    else:
        return np.allclose(0,led1_value,deviation)
    
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    time.sleep(1)
    pot1_value = 0
    pot2_value = 0
    move_pot(args["pot1"],pot1_value,driver)
    move_pot(args["pot2"],pot2_value,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot1_value, pot2_value) else 0)

    # test 2
    pot1_value = 1
    pot2_value = 0
    move_pot(args["pot1"],pot1_value,driver)
    move_pot(args["pot2"],pot2_value,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot1_value, pot2_value) else 0)

    # test 3
    pot1_value = 1
    pot2_value = 1
    move_pot(args["pot1"],pot1_value,driver)
    move_pot(args["pot2"],pot2_value,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot1_value, pot2_value) else 0)

    return res