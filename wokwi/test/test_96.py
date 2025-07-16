'''

**Task**:
You are tasked with programming an Arduino (uno) to control three individual LEDs (led1, led2, led3) and a 10-segment LED bar graph (bargraph1). The LEDs will blink sequentially, and the bar graph will dynamically reflect the number of active LEDs during each phase of the sequence.

**Detail Rules**:
1. **Initialization**: All LEDs and bar graph segments must be off when the system starts or resets.
2. **Blinking Sequence**:
   - The three LEDs (led1, led2, led3) must blink sequentially, each remaining active for exactly 2 seconds before switching to the next.
   - When each individual LED is active, the bar graph (bargraph1) must display a number of lit segments equal to the count of currently active LEDs (Pin A1-A10, 1 segment per active LED).
3. **Final Phase**:
   - After all three LEDs have completed their blinking sequence, the bar graph must light all 10 segments for 2 seconds before repeating the cycle.
4. **Timing**: Each state (LED active with corresponding bar graph segments, and final all-segments-lit phase) must persist for at least 2 seconds.

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

    led1_value = get_led_value(args['led1'],driver)
    led2_value = get_led_value(args['led2'],driver)
    led3_value = get_led_value(args['led3'],driver)

    bargraph_value = get_bargraph_value(args["bargraph1"],driver)

    current = [led1_value, led2_value, led3_value, *bargraph_value]

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    if (cur_time//2)%4 == 0:
        correct = [1,0,0] + [1,0,0,0,0,0,0,0,0,0]
    elif (cur_time//2)%4 == 1:
        correct = [0,1,0] + [1,0,0,0,0,0,0,0,0,0]
    elif (cur_time//2)%4 == 2:
        correct = [0,0,1] + [1,0,0,0,0,0,0,0,0,0]
    elif (cur_time//2)%4 == 3:
        correct = [0,0,0] + [1,1,1,1,1,1,1,1,1,1]


    return np.allclose(current, correct, deviation)
          
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    for _ in range(5):
        correct_sleep(_*2+2.2,clock)
        res["msg"].append(1 if test(clock, driver, args) else 0)




    return res