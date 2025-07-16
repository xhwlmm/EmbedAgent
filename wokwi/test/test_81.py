'''

**Task**:
You are tasked with programming an Arduino (uno) to control a two-digit number using three pushbuttons (btn1, btn2, btn3), displayed on two 7-segment displays (sevseg1, sevseg2) via shift registers (sr1, sr2). The LED bar graph (bargraph1) must visually indicate the tens digit of the current number.

**Detail Rules**:
1. **Initialization**:  
   - The 7-segment displays show "00".  
   - All LEDs in the bar graph (bargraph1) are off.  

2. **Button Interactions**:  
   - **btn1**: Increment the number by 1. If the number exceeds 99, reset to 0.  
   - **btn2**: Increment the number by 5. If the number exceeds 99, reset to 0.  
   - **btn3**: Reset the number to 0 immediately.  

3. **Display Updates**:  
   - The 7-segment displays must update within 0.15 seconds after a valid button press.  
   - The bar graph (bargraph1) must light up LEDs equal to the tens digit of the current number (e.g., 35 → 3 LEDs lit).  

4. **Debouncing**:  
   - Each button press must be debounced to prevent false triggers caused by mechanical vibrations.  

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

def test(clock, driver, args, click_num, deviation=0.2):
    sevseg1_value = get_sevseg_value(args["sevseg1"], driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"], driver)
    bargraph_value = get_bargraph_value(args["bargraph1"], driver)

    correct_sevseg1_value = sevseg_value[str(click_num//10)]
    correct_sevseg2_value = sevseg_value[str(click_num%10)]

    correct_bargraph_value = [1]*(click_num//10)+[0]*(10-(click_num//10))

    current = [*sevseg1_value, *sevseg2_value, *bargraph_value]
    correct = [*correct_sevseg1_value, *correct_sevseg2_value, *correct_bargraph_value]
    


    return np.allclose(current, correct, atol=deviation)


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: click the button1 once
    click_num = 0
    for _ in range(3):
        click_button(args['btn1'], actions)
        click_num += 1
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num) else 0)
    # test 2: click the button1 8 times
    for _ in range(3):
        click_button(args['btn2'], actions)
        click_num += 5
        time.sleep(0.5)

    res["msg"].append(1 if test(clock, driver, args, click_num) else 0)

    # test 3: click the button1
    click_button(args['btn3'], actions)
    click_num = 0
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num) else 0)
    
    return res