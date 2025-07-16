'''

**Task**:
You are tasked with programming an Arduino (uno) to create a synchronized light show using three RGB LEDs (rgb1, rgb2, rgb3) and a 5-segment LED bar graph (bargraph1). The system will cycle through five distinct phases, each controlling the RGB LEDs' colors and the bar graph's active segments.

**Detail Rules**:
1. **Phase Cycle**:
   - **Phase 1 (2 seconds)**: RGB1 (rgb1) displays red, and the bar graph (bargraph1) lights up 1 segment.
   - **Phase 2 (2 seconds)**: RGB2 (rgb2) displays green, and the bar graph lights up 2 segments.
   - **Phase 3 (2 seconds)**: RGB3 (rgb3) displays blue, and the bar graph lights up 3 segments.
   - **Phase 4 (2 seconds)**: RGB1 (red) and RGB2 (green) are both active, and the bar graph lights up 4 segments.
   - **Phase 5 (2 seconds)**: All three RGB LEDs (rgb1, rgb2, rgb3) display white, and the bar graph lights up all 5 segments.
   - note: bar graph lights up from pin:A1 to pin:A5
2. **Looping**: After Phase 5, the sequence restarts from Phase 1 indefinitely.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,get_sevseg_value, correct_sleep
from untils import sevseg_value

def test(clock, driver, args, deviation=0.2):
   colors = [
       [1, 0, 0]+[0, 0, 0]+[0, 0, 0],
       [0, 0, 0]+[0, 1, 0]+[0, 0, 0],
       [0, 0, 0]+[0, 0, 0]+[0, 0, 1],
       [1, 0, 0]+[0, 1, 0]+[0, 0, 0],
       [1, 1, 1]+[1, 1, 1]+[1, 1, 1]
   ]
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   rgb3_value = get_rgb_value(args['rgb3'], driver)
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
   bar_index = (cur_time//2)%5
   bar_correct = [1 if i <= bar_index else 0 for i in range(10)]
   correct_answer = colors[bar_index] + bar_correct
   current_answer = [*rgb1_value , *rgb2_value , *rgb3_value , *bargraph1_value]
   return np.allclose(correct_answer, current_answer, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(10.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(14.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 5
    correct_sleep(18.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    return res
