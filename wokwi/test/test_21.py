'''

Task:
You are tasked with programming an Arduino (uno) to control three servo motors (servo1, servo2, servo3). The servos should rotate in a synchronized sequence, where each servo moves to a specific angle, pauses for 2 seconds, and then moves to the next angle. The sequence should repeat indefinitely.

Detail Rules:
Initialization: Upon powering on or resetting, all servos (servo1, servo2, servo3) should start at their 0-degree position.
Sequence of Operation:
1. Servo1 moves to 0 degrees, Servo2 moves to 0 degrees, and Servo3 moves to 0 degrees. They move immediately and then maintain this position for 2 seconds.
2. Servo1 moves to 0 degrees, Servo2 moves to 45 degrees, and Servo3 moves to 90 degrees. They move immediately and then maintain this position for 2 seconds.
3. Servo1 moves to 45 degrees, Servo2 moves to 90 degrees, and Servo3 moves to 135 degrees. They move immediately and then maintain this position for 2 seconds.
4. Servo1 moves to 90 degrees, Servo2 moves to 135 degrees, and Servo3 moves to 180 degrees. They move immediately and then maintain this position for 2 seconds.
5. Servo1 moves to 135 degrees, Servo2 moves to 180 degrees, and Servo3 moves to 0 degrees. They move immediately and then maintain this position for 2 seconds.
6. Servo1 moves to 180 degrees, Servo2 moves to 0 degrees, and Servo3 moves to 45 degrees. They move immediately and then maintain this position for 2 seconds.
7. The sequence should then repeat from step 2.
All servo movements should be smooth.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,correct_sleep

def test(clock, driver, args):
    cur_time = get_clock(clock.text)

    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    servo3_value = get_servo_value(args['servo3'],driver)

    cur_t = int(cur_time+1)
    if cur_t % 2 == 1:
        cur_t += 1
    if cur_t <= 2:
        return abs(servo1_value - 0) < 1 and abs(servo2_value - 0) < 1 and abs(servo3_value - 0) < 1
    else:
        return abs(servo1_value - 45*((cur_t-4)%10)/2) < 1 and abs(servo2_value - 45*((cur_t-2)%10)/2) < 1 and abs(servo3_value - 45*((cur_t)%10)/2) < 1




def test_func(driver, clock, args, res):    # test 1
    correct_sleep(2.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(4.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(6.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(8.5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    

    return res