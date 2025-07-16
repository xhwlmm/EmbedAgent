'''

**Task**:
You are tasked with programming an Arduino (uno) to control three LEDs (led1, led2, led3), an RGB LED (rgb1), and two servo motors (servo1, servo2). The LEDs will blink in sequence, the RGB LED will cycle through colors, and the servo motors will sweep back and forth in synchronization with the LED sequence.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs (led1, led2, led3) should be off, the RGB LED (rgb1) should display red, and both servo motors (servo1, servo2) should be at their 0-degree position.
Servo Motors: The servo motors (servo1, servo2) should sweep from 0 degrees to 180 degrees and back to 0 degrees . Each sweep should take 2 seconds, and the servos should pause for 2 seconds at the 0-degree and 180-degree positions. This sequence should be infinitely repeated.
LED Sequence: The LEDs (led1, led2, led3) should blink in sequence, each flicker occurs when the servo motor (servo 1, servo 2) reaches 0 degrees or 180 degrees in scanning seconds, and then the next LED turns on. This sequence should be infinitely repeated.
RGB LED: The RGB LED (rgb1) should cycle through the colors red, green, and blue, each flicker occurs when the servo motor (servo 1, servo 2) reaches 0 degrees or 180 degrees in scanning seconds.
RGB flicker should be synchronized with LED.

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
    rgb1_value = get_rgb_value(args['rgb1'],driver)
    servo1_value = get_servo_value(args['servo1'], driver)
    servo2_value = get_servo_value(args['servo2'], driver)


    current = [led1_value, led2_value, led3_value, servo1_value, servo2_value, *rgb1_value]

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    if (cur_time//4)%3 == 0:
        co_led = [1,0,0]
    elif (cur_time//4)%3 == 1:
        co_led = [0,1,0]
    else:
        co_led = [0,0,1]

    if cur_time%8 < 2:
        co_servo = [0,0]
    elif cur_time%8 >=4 and cur_time%8 < 6:
        co_servo = [180,180]
    else:
        return 0 

    co_rgb = co_led

    correct = co_led + co_servo + co_rgb

    return np.allclose(current, correct, deviation)




def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(4.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(8.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(12.3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)



    return res