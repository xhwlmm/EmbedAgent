'''

**Task**:
You are tasked with programming an Arduino (uno) to control two LEDs (led1, led2), a 10-segment LED bar graph (bargraph1), and two servo motors (servo1, servo2). The LEDs and the bar graph will display a pattern based on the movement of the servo motors. The servos will sweep between 0° and 180°, and the LEDs and bar graph will light up in sync with the servo positions.

**Detail Rules**:
Initialization: Upon powering on or resetting, both servos (servo1, servo2) should start at 0°, and all LEDs (led1, led2, bargraph1) should be off.
Servo Movement:
1. Servo1 (servo1) will sweep from 0° to 180° in increments of 10°, pausing for 2000 milliseconds at each step.
2. Servo2 (servo2) will sweep from 180° to 0° in decrements of 10°, pausing for 2000 milliseconds at each step.
LED and Bar Graph Behavior:
1. LED1 (led1) will turn on when Servo1 is between 0° and 90°, and turn off when Servo1 is between 91° and 180°.
2. LED2 (led2) will turn on when Servo2 is between 90° and 180°, and turn off when Servo2 is between 0° and 89°.
3. The LED bar graph (bargraph1) will light up segments corresponding to the current position of Servo1. For example:
   - If Servo1 is at 0°, no segments are lit.
   - If Servo1 is at 90°, 5 segments are lit.
   - If Servo1 is at 180°, all 10 segments are lit.
The system should continuously repeat the servo movement and LED/bar graph behavior.

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
    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    led1_value = get_led_value(args['led1'],driver)
    led2_value = get_led_value(args['led2'],driver)
    servo1_value = get_servo_value(args["servo1"], driver)
    servo2_value = get_servo_value(args["servo2"], driver)
    bargraph1_value = get_bargraph_value(args["bargraph1"], driver)
    if (cur_time // 36) % 2 == 0:
        cur_time = cur_time % 36
    else:
        cur_time = 36 - (cur_time % 36)
    cur_time = cur_time // 2
    correct_servo1 = 0+10*cur_time
    correct_servo2 = 180-10*cur_time
    correct_led1 = 1 if correct_servo1 < 90 else 0
    correct_led2 = 1 if correct_servo2 > 90 else 0
    correct_bargraph1 = []
    if correct_servo1 < 90:
        correct_bargraph1 = [0]*10
    if 90 <= correct_servo1 < 180:
        correct_bargraph1 = [1]*5+[0]*5
    if correct_servo1 == 180:
        correct_bargraph1 = [1]*10
    correct = [correct_servo1,correct_servo2,correct_led1,correct_led2,*correct_bargraph1]
    current = [servo1_value,servo2_value,led1_value,led2_value,*bargraph1_value]
    return np.allclose(current, correct, atol=deviation)
        
          
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(2.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(20.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(36.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res