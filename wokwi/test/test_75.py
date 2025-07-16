'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 10-segment LED bar graph (bargraph1) using two slide potentiometers (pot1, pot2) and a pushbutton (btn1). The LED bar graph will display a value determined by the selected potentiometer, and the pushbutton will toggle between the two potentiometers as the active input source.

**Detail Rules**:
1. **Initialization**: All LEDs in the bar graph (bargraph1) must be off when the system starts or resets.
2. **Button Interaction**:
   - Each valid press of the button (btn1) toggles the active input between pot1 and pot2. (First press selects pot1, second press selects pot2, and so on.)
   - A valid press is defined as a button state change lasting at least 0.15 seconds to account for debouncing.
3. **Display Behavior**:
   - When pot1 is active, the number of lit LEDs corresponds to its analog value (0-1023 mapped to 0-10 LEDs). (from pin:A1 to A10)
   - When pot2 is active, the number of lit LEDs corresponds to its analog value (0-1023 mapped to 0-10 LEDs). (from pin:A1 to A10)
   - The bar graph must update continuously to reflect the current potentiometer value.
4. **Boundary Conditions**: If a potentiometer's value maps to 0, all LEDs must remain off. If it maps to 10, all LEDs must be fully lit.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,get_bargraph_value,click_button,get_servo_value

def test(clock, driver, args, click_num, pot1, pot2, deviation=0.2):
    bargraph_1 = get_bargraph_value(args["bargraph1"], driver)

    current = [*bargraph_1]
    correct = []
    if click_num%2 == 0:
        correct = [pot1]*10
    else:
        correct = [pot2]*10

    return np.allclose(current, correct, atol=deviation)



def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    click_num = 0
    pot1 = 0
    pot2 = 0
    res["msg"].append(1 if test(clock, driver, args, click_num, pot1, pot2) else 0)
    # test 2: click the button
    click_num = 0
    pot1 = 1
    pot2 = 0
    move_pot(args["pot1"], pot1, driver)
    move_pot(args["pot2"], pot2, driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num, pot1, pot2) else 0)

    # test 3: click the button twice
    click_num = 1
    pot1 = 1
    pot2 = 0
    move_pot(args["pot1"], pot1, driver)
    move_pot(args["pot2"], pot2, driver)
    click_button(args['btn1'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num, pot1, pot2) else 0)

    # test 4: click the button three times
    click_num = 1
    pot1 = 1
    pot2 = 1
    move_pot(args["pot1"], pot1, driver)
    move_pot(args["pot2"], pot2, driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num, pot1, pot2) else 0)
    
    return res