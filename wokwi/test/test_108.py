'''

**Task**:
You are tasked with programming an Arduino (uno) to control a single-color LED (led1) and three RGB LEDs (rgb1, rgb2, rgb3). The single-color LED will act as a status indicator, while the RGB LEDs will cycle through a sequence of colors. The single-color LED should blink at a fixed interval, and the RGB LEDs should transition through a predefined sequence of colors, with each color displayed for 2 seconds.

**Detail Rules**:
1. **Single-color LED (led1)**:
   - The LED should blink on and off with a 2-second interval (2 second on, 2 second off).
   - This blinking should continue indefinitely.

2. **RGB LEDs (rgb1, rgb2, rgb3)**:
   - All three RGB LEDs should synchronously cycle through the following sequence of colors:
     - Red (R=255, G=0, B=0)
     - Green (R=0, G=255, B=0)
     - Blue (R=0, G=0, B=255)
     - Yellow (R=255, G=255, B=0)
     - Cyan (R=0, G=255, B=255)
     - Magenta (R=255, G=0, B=255)
     - White (R=255, G=255, B=255)
   - Each color should be displayed for 2 seconds before transitioning to the next color.
   - After reaching the last color (White), the sequence should restart from Red.

3. **Synchronization**:
   - The blinking of the single-color LED (led1) and the color transitions of the RGB LEDs should operate independently but simultaneously.

4. **Initial State**:
   - On startup, the single-color LED (led1) should be off, and the RGB LEDs (rgb1, rgb2, rgb3) should display the first color in the sequence (Red).

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



def test(clock, driver, args, deviation=0.2):
    
    colors = [
        [1,0,0],
        [0,1,0],
        [0,0,1],
        [1,1,0],
        [0,1,1],
        [1,0,1],
        [1,1,1]
    ]


    led1_value = get_led_value(args['led1'],driver)
    rgb1_value = get_rgb_value(args['rgb1'],driver)
    rgb2_value = get_rgb_value(args['rgb2'],driver)
    rgb3_value = get_rgb_value(args['rgb3'],driver)


    current = [led1_value, *rgb1_value, *rgb2_value, *rgb3_value]

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)

    correct = [(cur_time//2)%2, *colors[(cur_time//2)%7], *colors[(cur_time//2)%7], *colors[(cur_time//2)%7]]




    return np.allclose(current, correct, deviation)




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

    correct_sleep(18.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res