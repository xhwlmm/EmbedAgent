'''

**Task**:
You are tasked with programming an Arduino (uno) to control an LED bar graph (bargraph1) and two RGB LEDs (rgb1, rgb2). The bar graph will display a sequential pattern, while the RGB LEDs will change colors based on the active segment of the bar graph.

**Detail Rules**:
1. **Initialization**: All components start in an off state when powered on or reset.
2. **Bar Graph Sequence**:
   - The bar graph (bargraph1) lights up LEDs sequentially from A1 to A8, one at a time.
   - Each LED remains lit for **2 seconds** before moving to the next.
   - After reaching A8, the sequence restarts from A1.
3. **RGB LED Behavior**:
   - When LEDs A1-A4 are lit, rgb1 must display **red** and rgb2 must display **blue**.
   - When LEDs A5-A8 are lit, rgb1 must display **green** and rgb2 must display **yellow** (red + green).

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,get_sevseg_value
from untils import sevseg_value

def test(clock, driver, args, deviation=0.2):
   colors = [
       [1, 0, 0]+[0, 0, 1],
       [0, 1, 0]+[1, 1, 0]
   ]
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
   bar_index = (cur_time//2)%8
   bar_correct = [0 for i in range(10)]
   bar_correct[bar_index] = 1
   correct_answer = colors[((cur_time//2)%8)//4] + bar_correct
   current_answer = [*rgb1_value ,*rgb2_value ,*bargraph1_value]
   return np.allclose(correct_answer, current_answer, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    time.sleep(3.5)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    time.sleep(6)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    time.sleep(8)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res