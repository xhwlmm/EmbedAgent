'''

**Task**:
You are tasked with programming an Arduino (uno) to control three LEDs (led1, led2, led3) and two servo motors (servo1, servo2). The LEDs will act as indicators for the servo positions, and the servos will move in a synchronized pattern. The LEDs will light up in sequence to indicate the current state of the servos.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs (led1, led2, led3) should be off, and both servos (servo1, servo2) should be at their 0-degree position.
Servo Movement:
1.First Servo1 (servo1) will start at 0 degrees and increment its angle by 30 degrees every 2 seconds (immediately move and then stay for 2 seconds) until it reaches 180 degrees.
2.Then Servo2 (servo2) will start at 180 degrees and decrement its angle by 30 degrees every 2 seconds (immediately move and then stay for 2 seconds) until it reaches 0 degrees.
LED Indication:
1. When Servo1 is moving, LED1 (led1) will light up.
2. When Servo2 is moving, LED2 (led2) will light up.
3. When both servos reach their target positions (180 degrees for Servo1 and 0 degrees for Servo2), LED3 (led3) will light up for 2 seconds before the cycle repeats.
Cycle Repetition: After both servos reach their target positions and LED3 (led3) lights up, the servos will reset to their initial positions (0 degrees for Servo1 and 180 degrees for Servo2), and the cycle will repeat.

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


def test(clock, driver, args, deviation = 0.2):
    led1_value = get_led_value(args['led1'], driver)
    led2_value = get_led_value(args['led2'], driver)
    led3_value = get_led_value(args['led3'], driver)
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)%26
    current = [led1_value, led2_value, led3_value, servo1_value, servo2_value]

    if cur_time < 12:
        correct = [1,0,0,cur_time//2*30,180]
    elif cur_time < 24:
        correct = [0,1,0,180,180-(cur_time-12)//2*30]
    elif cur_time < 26:
        correct = [0,0,1,180,0]
    return np.allclose(current, correct, deviation)



def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init 
    time.sleep(0.7)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2: click the button1 
    correct_sleep(8.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3: click the button2 
    correct_sleep(16.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4: 
    correct_sleep(24.3,clock)

    res["msg"].append(1 if test(clock, driver, args) else 0)



    return res
