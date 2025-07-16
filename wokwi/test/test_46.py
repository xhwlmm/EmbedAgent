'''

**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) and three servo motors (servo1, servo2, servo3). The RGB LED will cycle through a sequence of colors, and each servo motor will move to a specific angle based on the current color of the RGB LED. The system should continuously cycle through the color sequence, with each color and corresponding servo positions maintained for at least 2 seconds.

**Detail Rules**:
1. **RGB LED Sequence**:
   - The RGB LED (rgb1) should cycle through the following colors in order: Red, Green, Blue, Yellow, Cyan, Magenta, White.
   - Each color should be displayed for 2 seconds before transitioning to the next color.

2. **Servo Motor Behavior**:
   - When the RGB LED is Red, servo1 should move to 0°, servo2 to 90°, and servo3 to 180°.
   - When the RGB LED is Green, servo1 should move to 90°, servo2 to 180°, and servo3 to 0°.
   - When the RGB LED is Blue, servo1 should move to 180°, servo2 to 0°, and servo3 to 90°.
   - When the RGB LED is Yellow, servo1 should move to 45°, servo2 to 135°, and servo3 to 225° (if supported, otherwise 180°).
   - When the RGB LED is Cyan, servo1 should move to 135°, servo2 to 225° (if supported, otherwise 180°), and servo3 to 45°.
   - When the RGB LED is Magenta, servo1 should move to 225° (if supported, otherwise 180°), servo2 to 45°, and servo3 to 135°.
   - When the RGB LED is White, all servos should return to their initial positions: servo1 to 0°, servo2 to 90°, and servo3 to 180°.

3. **Timing**:
   - Each color and corresponding servo positions should be maintained for 2 seconds before transitioning to the next state.

4. **Hardware Usage**:
   - The RGB LED (rgb1) and all three servo motors (servo1, servo2, servo3) must be used in the solution.

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
       [1, 0, 0],
       [0, 1, 0],
       [0, 0, 1],
       [1, 1, 0],
       [0, 1, 1],
       [1, 0, 1],
       [1, 1, 1]
   ]
   servo_digrees = [
       [0, 90, 180],
       [90, 180, 0],
       [180, 0, 90],
       [45, 135, 180],
       [135, 180, 45],
       [180, 45, 135],
       [0, 90, 180]
   ]
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   servo3_value = get_servo_value(args['servo3'],driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   correct_index = (cur_time // 2) % len(colors)
   correct_answer = [*colors[correct_index], *servo_digrees[correct_index]]
   current_answer = [*rgb1_value, servo1_value, servo2_value, servo3_value]
   return np.allclose(correct_answer, current_answer, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(10.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res
