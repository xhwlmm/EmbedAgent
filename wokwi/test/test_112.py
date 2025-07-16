'''

**Task**:
You are tasked with programming an Arduino (uno) to control three single-color LEDs (led1, led2, led3) and two RGB LEDs (rgb1, rgb2) using two slide potentiometers (pot1, pot2). The slide potentiometers will control the brightness of the single-color LEDs and the color of the RGB LEDs. The single-color LEDs will act as indicators for the potentiometer values, while the RGB LEDs will display a color gradient based on the combined values of the potentiometers.

**Detail Rules**:
1. **Single-Color LEDs (led1, led2, led3)**:
   - The brightness of each single-color LED is controlled by the value of one potentiometer.
   - `led1` brightness is controlled by `pot1`.
   - `led2` brightness is controlled by `pot2`.
   - If both `pot1` and `pot2` are at their maximum value (1023),
`led3` should be on.
   - The brightness of each LED should be updated continuously based on the potentiometer values.

2. **RGB LEDs (rgb1, rgb2)**:
   - The color of both RGB LEDs is determined by the combined values of `pot1` and `pot2`.
   - The red component is controlled by `pot1`.
   - The green component is controlled by `pot2`.
   - If both `pot1` and `pot2` are at their maximum value (1023), the RGB LEDs should display white.
   - The RGB LEDs should display the same color gradient, updated continuously based on the potentiometer values.

3. **Potentiometer Values**:
   - The values of `pot1` and `pot2` range from 0 to 1023.
   - These values should be mapped to appropriate ranges for controlling LED brightness (0-255) and RGB color components (0-255).

4. **State Maintenance**:
   - The system should continuously update the LED states based on the potentiometer values.


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
    rgb1 = get_rgb_value(args['rgb1'],driver)
    rgb2 = get_rgb_value(args['rgb2'],driver)

    led1 = get_led_value(args["led1"],driver)
    led2 = get_led_value(args["led2"],driver)
    led3 = get_led_value(args["led3"],driver)


    current = [led1,led2,led3,*rgb1,*rgb2]

    correct = [pot_pos[0],pot_pos[1],round((pot_pos[0]+pot_pos[1])/2),pot_pos[0],pot_pos[1],(pot_pos[0]+pot_pos[1])//2,pot_pos[0],pot_pos[1],(pot_pos[0]+pot_pos[1])//2]

    return np.allclose(current, correct, deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    pot_pos = [0,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    # test 2
    pot_pos = [1,0]
    move_pot(args["pot1"],1,driver)
    move_pot(args["pot2"],0,driver)

    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    # test 3
    pot_pos = [1,1]
    move_pot(args["pot1"],1,driver)
    move_pot(args["pot2"],1,driver)

    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)

    pot_pos = [0,1]
    move_pot(args["pot1"],0,driver)
    move_pot(args["pot2"],1,driver)

    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)
    
    return res