'''

**Task**:
You are tasked with programming an Arduino (uno) to control a single-color LED (led1), two RGB LEDs (rgb1, rgb2), and three servo motors (servo1, servo2, servo3). The system should create a synchronized light and motion display. The LED and RGB LEDs will change their brightness and colors, while the servo motors will move to specific angles in a coordinated manner.

**Detail Rules**:
Initialization: Upon powering on or resetting, the LED (led1) should be off, the RGB LEDs (rgb1, rgb2) should display red light, and the servo motors (servo1, servo2, servo3) should be at their 0-degree position.
Operation:
1. The LED (led1) should blink on and off with a 2-second interval.
2. The RGB LEDs (rgb1, rgb2) should cycle through the colors of the rainbow (red, green, blue, yellow, cyan, magenta, white) in sequence, with each color displayed for 2 seconds.
3. The servo motors (servo 1, servo 2, servo 3) should move in synchronous mode:
-If Servo1 is at 0 degrees, scan to 180 degrees; If at 180 degrees, scan to 0 degrees. (init at 0 degrees)
-If Servo2 is at 180 degrees, it will scan to 0 degrees; If at 0 degrees, scan to 180 degrees. (init at 180 degrees)
-If Servo3 is at 90 degrees, it will scan to 135 degrees; If it is at 135 degrees, scan to 90 degrees. (init at 90 degrees)
Each scan should have a 2-second interval.
4. The LED blinking, RGB color cycling, and servo movements should all be synchronized and repeat continuously.

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


    rgb1_value = get_rgb_value(args['rgb1'], driver)
    rgb2_value = get_rgb_value(args['rgb2'], driver)

    led1 = get_led_value(args["led1"],driver)

    servo1_value = get_servo_value(args['servo1'], driver)
    servo2_value = get_servo_value(args['servo2'], driver)
    servo3_value = get_servo_value(args['servo3'], driver)


    current = [led1,*rgb1_value,*rgb2_value,servo1_value,servo2_value,servo3_value]

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    correct = [(cur_time // 2 )%2,*colors[(cur_time//2)%7],*colors[(cur_time//2)%7],180*((cur_time//2)%2),180*(((cur_time//2)+1)%2),90+45*((cur_time//2)%2)]

    return np.allclose(current, correct, deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(2.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(10.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(14.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    
    return res