'''

**Task**:
You are tasked with programming an Arduino (uno) to control three LEDs (led1, led2, led3), two 7-segment displays (sevseg1, sevseg2), and a slide potentiometer (pot1). The potentiometer will determine the brightness level of the LEDs and the number displayed on the 7-segment displays. The LEDs will light up in sequence based on the potentiometer's value, and the 7-segment displays will show a two-digit number corresponding to the potentiometer's value.

**Detail Rules**:
1. **Initialization**: Upon powering on or resetting, all LEDs (led1, led2, led3) should be off, and the 7-segment displays (sevseg1, sevseg2) should show "00".
2. **Potentiometer Interaction**:
   - The potentiometer (pot1) value ranges from 0 to 1023. This value should be mapped to a range of 0 to 99 for display on the 7-segment displays.
   - The mapped value should be displayed on the two 7-segment displays, with the tens digit on one display (sevseg1) and the units digit on the other (sevseg2).
3. **LED Control**:
   - If the mapped potentiometer value is between 0 and 33, only LED1 (led1) should light up.
   - If the mapped value is between 34 and 66, LED1 (led1) and LED2 (led2) should light up.
   - If the mapped value is between 67 and 99, all three LEDs (led1, led2, led3) should light up.
4. **Display Update**: The 7-segment displays and LEDs should update continuously based on the potentiometer's current value.
5. **State Maintenance**: Each state (LEDs and display) should be maintained for at least 2 seconds to allow for verification.

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
    sevseg1_value = get_sevseg_value(args["sevseg1"],driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"],driver)

    led1 = get_led_value(args["led1"],driver)
    led2 = get_led_value(args["led2"],driver)
    led3 = get_led_value(args["led3"],driver)


    current = [led1,led2,led3,*sevseg1_value,*sevseg2_value]

    if pot_pos == 1:
        correct = [1,1,1, *sevseg_value['9'], *sevseg_value['9']] 
    elif pot_pos == 0:
        correct = [1,0,0, *sevseg_value['0'], *sevseg_value['0']]
    else:
        return 0

    return np.allclose(current, correct, deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    pot_pos = 0
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    # test 2
    pot_pos = 1
    move_pot(args["pot1"],1,driver)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    # test 3
    pot_pos = 0
    move_pot(args["pot1"],0,driver)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    
    return res