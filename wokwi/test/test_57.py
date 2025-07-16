'''

**Task**:
You are tasked with programming an Arduino (uno) to control three RGB LEDs (rgb1, rgb2, rgb3) and two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2). The RGB LEDs will cycle through a sequence of colors, and the 7-segment displays will show a countdown timer synchronized with the color changes. The countdown starts at 99 and decreases by 1 every 2 seconds. When the countdown reaches 0, it resets to 99, and the RGB LEDs restart their color sequence.

**Detail Rules**:
1. **RGB LEDs (rgb1, rgb2, rgb3)**:
   - The RGB LEDs will cycle through the following sequence of colors, each lasting 2 seconds:
     - Red (rgb1: red on, green and blue off; rgb2 and rgb3: off)
     - Green (rgb2: green on, red and blue off; rgb1 and rgb3: off)
     - Blue (rgb3: blue on, red and green off; rgb1 and rgb2: off)
     - Purple (rgb1: red and blue on, green off; rgb2 and rgb3: off)
     - Yellow (rgb2: red and green on, blue off; rgb1 and rgb3: off)
     - Cyan (rgb3: green and blue on, red off; rgb1 and rgb2: off)
   - After the last color in the sequence, the cycle repeats.

2. **7-Segment Displays (sevseg1, sevseg2)**:
   - The displays will show a countdown timer starting at 99.
   - The countdown decreases by 1 every 2 seconds.
   - When the countdown reaches 0, it resets to 99, and the RGB LEDs restart their color sequence.

3. **Synchronization**:
   - The countdown timer and the RGB LED color sequence must be synchronized, with each color change and countdown decrement occurring simultaneously every 2 seconds.

4. **Initial State**:
   - On startup, the RGB LEDs should display the first color in the sequence (red), and the 7-segment displays should show "99".

5. **Reset Condition**:
   - When the countdown reaches 0, the timer resets to 99, and the RGB LEDs restart their color sequence from red.

6. **Hardware Usage**:
   - All components (RGB LEDs, 7-segment displays, shift registers) must be used as described.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,get_sevseg_value,correct_sleep
from untils import sevseg_value

def test(clock, driver, args, deviation=0.2):
   colors = [
       [1, 0, 0]+[0, 0, 0]+[0, 0, 0],
       [0, 0, 0]+[0, 1, 0]+[0, 0, 0],
       [0, 0, 0]+[0, 0, 0]+[0, 0, 1],
       [1, 0, 1]+[0, 0, 0]+[0, 0, 0],
       [0, 0, 0]+[1, 1, 0]+[0, 0, 0],
       [0, 0, 0]+[0, 0, 0]+[0, 1, 1],
   ]
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   rgb3_value = get_rgb_value(args['rgb3'], driver)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   sevseg2_value = get_sevseg_value(args['sevseg2'], driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_index = (cur_time // 2) % 6
   correct_num = 99 - (cur_time // 2) % 100
   digit = correct_num % 10
   tens = correct_num // 10
   correct_answer = [*colors[correct_index], *sevseg_value[str(tens)], *sevseg_value[str(digit)]]
   current_answer = [*rgb1_value, *rgb2_value, *rgb3_value, *sevseg1_value, *sevseg2_value]
   return np.allclose(correct_answer, current_answer, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(0.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(2.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(4.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(6.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 5
    correct_sleep(8.5, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res