'''

**Task**:
You are tasked with programming an Arduino (uno) to create a synchronized light sequence using a regular LED (led1), three RGB LEDs (rgb1, rgb2, rgb3), and a 4-segment LED bar graph (bargraph1). The system must cycle through distinct stages where each hardware component exhibits specific behaviors.

**Detail Rules**:
1. **Initialization**: All LEDs must start in an off state.
2. **Stage Cycling**:
   - The system progresses through four stages, each lasting exactly 2 seconds.
   - After completing Stage 4, the sequence repeats from Stage 1.
3. **Stage 1 (0-2 seconds)**:
   - The regular LED (led1) is turned off.
   - RGB1 (rgb1) displays red; RGB2 (rgb2) and RGB3 (rgb3) remain off.
   - The bar graph (bargraph1) lights up 1 segment.(PIN A1)
4. **Stage 2 (2-4 seconds)**:
   - The regular LED lights up.
   - RGB1 displays green, RGB2 displays blue, and RGB3 remains off.
   - The bar graph lights up 2 segments.(PIN A1-A2)
5. **Stage 3 (4-6 seconds)**:
   - The regular LED (led1) is turned off.
   - RGB1 displays blue, RGB2 displays red, and RGB3 displays green.
   - The bar graph lights up 3 segments.(PIN A1-A3)
6. **Stage 4 (6-8 seconds)**:
   - The regular LED lights up.
   - All RGB LEDs display white (all colors activated).
   - The bar graph lights up all 4 segments.(PIN A1-A4)

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
        [1,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,1,0,0,0],
        [0,0,1,1,0,0,0,1,0],
        [1,1,1,1,1,1,1,1,1]
    ]

    led1 = get_led_value(args['led1'],driver)
    rgb1_value = get_rgb_value(args["rgb1"],driver)
    rgb2_value = get_rgb_value(args["rgb2"],driver)
    rgb3_value = get_rgb_value(args["rgb3"],driver)
    bar1_value = get_bargraph_value(args["bargraph1"],driver)

    current = [led1,*rgb1_value,*rgb2_value,*rgb3_value,*bar1_value]

    cur_time = get_clock(clock.text)

    cur_time = int(cur_time)

    correct = [(cur_time//2)%2,*colors[(cur_time//2)%4]] + [1]*((cur_time//2)%4+1) + [0]*(9-(cur_time//2)%4)



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