'''

**Task**:
You are tasked with programming an Arduino (uno) to synchronize two servo motors (servo1, servo2), two RGB LEDs (rgb1, rgb2), and a 6-segment LED bar graph (bargraph1). The servos will rotate in fixed increments, while the RGB LEDs and bar graph dynamically reflect their positions.

**Detail Rules**:
1. **Initialization**: 
   - Both servos (servo1, servo2) start at 0°.
   - Both RGB LEDs (rgb1, rgb2) remain off.
   - The bar graph (bargraph1) shows no lit LEDs.

2. **Servo Motion**:
   - Every 2 seconds, both servos increment their angles by 30° simultaneously.
   - After reaching 180°, both servos reset to 0° and repeat the cycle.

3. **RGB LED Behavior**:
   - rgb1 show red color.
   - rgb2 show blue color.

4. **Bar Graph Display**:
   - The number of lit LEDs corresponds to the average angle of the servos. When the servos at [0°, 90°], the first RGB LED is lit. When at (90°, 180°], both RGB LEDs are lit.
   - All LEDs reset when the servos return to 0°.
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
       [1, 0, 0]+[0, 0, 0],
       [1, 0, 0]+[0, 0, 1],
   ]
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   rgb2_value = get_rgb_value(args['rgb2'], driver)
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   index = (cur_time//2)%7
   bar_correct = [1 if i < index else 0 for i in range(10)]
   correct_answer = colors[index//4] + bar_correct + [servo1_value, servo2_value]
   current_answer = [*rgb1_value , *rgb2_value , *bargraph1_value, servo1_value, servo2_value]
   return np.allclose(correct_answer, current_answer, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(4.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(8.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(10.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    return res