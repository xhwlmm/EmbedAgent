'''

**Task**:
You are tasked with programming an Arduino (uno) to control two LEDs (led1, led2) and three servo motors (servo1, servo2, servo3). The LEDs will act as indicators, and the servos will rotate in a synchronized pattern. The LEDs will blink alternately, and the servos will move in a sequence: servo1 to 0°, servo2 to 90°, and servo3 to 180°, then reverse the sequence. The LEDs and servos should operate in a continuous loop.

**Detail Rules**:
Initialization: Upon powering on or resetting, both LEDs (led1, led2) should be off, and all servos (servo1, servo2, servo3) should be at their initial positions (0°).
LED Behavior: The LEDs should blink alternately every 2000 milliseconds. When led1 is on, led2 should be off, and vice versa.
Servo Behavior: The servos should move in the following sequence:
1. servo1 moves to 0°, servo2 moves to 90°, and servo3 moves to 180°. This state should be maintained for 2 seconds.
2. servo1 moves to 180°, servo2 moves to 0°, and servo3 moves to 90°. This state should be maintained for 2 seconds.
3. The sequence should repeat continuously.
Synchronization: The LED blinking and servo movements should be synchronized, with the LEDs blinking continuously while the servos move through their sequence.

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
    servo1_value = get_servo_value(args["servo1"], driver)
    servo2_value = get_servo_value(args["servo2"], driver)
    servo3_value = get_servo_value(args["servo3"], driver)
    led1_value = get_led_value(args['led1'], driver)
    led2_value = get_led_value(args['led2'], driver)

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    current = [servo1_value, servo2_value, servo3_value, led1_value, led2_value]

    if (cur_time//2)%2 == 0:
        correct = [0,90,180,1,0]
    else:
        correct = [180,0,90,0,1]
    
    return np.allclose(current, correct, deviation)
    
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(1,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(3,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(5,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res