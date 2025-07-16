'''

**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2) and a slide potentiometer (pot1). The 7-segment displays will show a two-digit number, where one display represents the tens digit and the other represents the units digit. The slide potentiometer will control the displayed number, with its value mapped to a range between 0 and 99. The number should update dynamically as the potentiometer is adjusted.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00".
Potentiometer Interaction: The value of the slide potentiometer (pot1) should be mapped to a range between 0 and 99. The mapped value should be displayed on the two 7-segment displays, with the tens digit on one display (sevseg1) and the units digit on the other (sevseg2).
Display Update: The 7-segment displays should update dynamically to reflect the current value of the potentiometer.
Range Handling: If the potentiometer value maps to a number outside the 0-99 range, the displays should show "00".

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_sevseg_value
from untils import sevseg_value

def test_func(driver, clock, args, res): 
    deviation=0.2
    # test 1 
    time.sleep(0.5)
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
    if np.allclose(sevseg1_value,sevseg_value['0'],rtol=deviation) and np.allclose(sevseg2_value,sevseg_value['0'],rtol=deviation):
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 2
    move_pot(args['pot1'],1,driver)
    time.sleep(0.5)
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
    if np.allclose(sevseg1_value,sevseg_value['9'],rtol=deviation) and np.allclose(sevseg2_value,sevseg_value['9'],rtol=deviation):
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 3
    move_pot(args['pot1'],0,driver)
    time.sleep(0.5)
    sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
    sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
    if np.allclose(sevseg1_value,sevseg_value['0'],rtol=deviation) and np.allclose(sevseg2_value,sevseg_value['0'],rtol=deviation):
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    return res