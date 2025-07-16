'''

**Task**:
You are tasked with programming an Arduino (uno) to control a single-color LED (led1), an RGB LED (rgb1), and two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2). Monochrome LEDs will flash at 2-second intervals, RGB LEDs will cycle in a predefined color order, and 7-segment displays will repeat counting from 00 to 99. The 7-segment monitor should be updated every 2 seconds, and the RGB LED should change color every 2 seconds.

**Detail Rules**:
1. **Single-color LED (led1)**:
   - The LED is initially turned off.
   - The LED should flash at intervals of 2 seconds (2 seconds on, 2 seconds off).
   - This blinking should continue indefinitely.

2. **RGB LED (rgb1)**:
   - The RGB LED should cycle through the following colors in sequence: Red, Green, Blue, Yellow, Cyan, Magenta, White.
   - Each color should be displayed for 2 seconds before transitioning to the next color.
   - The sequence should repeat indefinitely.

3. **7-segment displays (sevseg1, sevseg2)**:
   - The displays should show a two-digit number starting from 00 and incrementing by 1 every 2 second.
   -When the count reaches 99, it should reset to 00 after two second and continue counting.
   - The tens digit should be displayed on one 7-segment display (sevseg1), and the units digit should be displayed on the other (sevseg2).

4. **Shift registers (sr1, sr2)**:
   - The shift registers should be used to control the 7-segment displays.
   - The Arduino should send the appropriate data to the shift registers to display the correct digits on the 7-segment displays.

5. **Timing**:
   - Monochrome LED, RGB LED, and 7-segment displays should be updated every 2 seconds.
   - All timing should be precise and maintained for 2 seconds for verification purposes.

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
from untils import sevseg_value,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,get_bargraph_value,click_button,get_servo_value,correct_sleep



def test(clock, driver, args,deviation=0.2):

    colors = [
        [1,0,0],
        [0,1,0],
        [0,0,1],
        [1,1,0],
        [0,1,1],
        [1,0,1],
        [1,1,1]
    ]

    led1 = get_led_value(args['led1'],driver)
    rgb1_value = get_rgb_value(args["rgb1"],driver)
    sevseg1_value = get_sevseg_value(args["sevseg1"],driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"],driver)

    current = [led1,*rgb1_value,*sevseg1_value,*sevseg2_value]

    cur_time = get_clock(clock.text)

    cur_time = int(cur_time)

    num = (cur_time//2)%100
    correct = [num%2,*colors[(cur_time//2%7)],*sevseg_value[str(num//10)],*sevseg_value[str(num%10)]]

    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(2.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(6.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(10.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(14.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res