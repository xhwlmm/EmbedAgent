'''

**Task**:
You are tasked with programming an Arduino (uno) to control two LEDs (led1, led2), a 7-segment display (sevseg1), and two servo motors (servo1, servo2). The LEDs will blink alternately, the 7-segment display will count from 0 to 9 repeatedly, and the servo motors will sweep between 0° and 180° in opposite directions. The system should operate continuously, with each component functioning independently.

**Detail Rules**:
1. **LEDs (led1, led2)**:
   - The LEDs should blink alternately, with each LED staying on for 2 second and off for 2 second.
   - When one LED is on, the other should be off, and vice versa.
   - First led1 off, led2 on, then led1 on, led2 off.

2. **7-Segment Display (sevseg1)**:
   - The display should count from 0 to 9 repeatedly, with each number displayed for 2 seconds.
   - The count should reset to 0 after reaching 9.

3. **Servo Motors (servo1, servo2)**:
   - The first servo (servo1) should sweep from 0° to 180° and back to 0° continuously, with each sweep taking 4 seconds.
   - The second servo (servo2) should sweep from 180° to 0° and back to 180° continuously, with each sweep taking 4 seconds.
   - The servos should move in opposite directions at the same time. 
   - when move to 180° or 0°, the servo should stop for 2 second and then continue sweep.
   - Before the servo start the first sweep, althoug the servo is in 0° or 180°, the servo don't need to stop for 2 second.
4. **System Operation**:
   - All components should operate simultaneously and independently.

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
    servo1 = get_servo_value(args["servo1"], driver)
    servo2 = get_servo_value(args["servo2"], driver)
    led1 = get_led_value(args["led1"],driver)
    led2 = get_led_value(args["led2"],driver)
    sevseg = get_sevseg_value(args["sevseg1"],driver)
    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    correct_num = cur_time // 2
    if correct_num % 2 == 0:
        correct_led = [0, 1]
    else:
        correct_led = [1, 0]
    correct_sevseg = sevseg_value[str(correct_num%10)]
    if (cur_time // 6) % 2 == 0:
        correct_servo = [180, 0]
    else:
        correct_servo = [0, 180]
    correct = [*correct_led, *correct_sevseg, *correct_servo]
    current = [led1, led2, *sevseg, servo1, servo2]
    return np.allclose(current, correct, atol=deviation)

def test_func(driver, clock, args, res):
    # test 1
    correct_sleep(4.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(10.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(16.2, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    
    return res