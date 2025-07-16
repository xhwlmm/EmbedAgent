'''

**Task**:
You are tasked with programming an Arduino (uno) to control three LEDs (led1, led2, led3), two 7-segment displays (sevseg1, sevseg2), and three servos (servo1, servo2, servo3). The LEDs will act as indicators, the 7-segment displays will show a two-digit number, and the servos will rotate to specific angles based on the displayed number. The system should increment the displayed number by 1 every 2 seconds, and the LEDs and servos should update their states accordingly.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00", all LEDs should be off, and all servos should be at 0 degrees.
Number Increment: Every 2 seconds, the displayed number should increment by 1. If the number exceeds 99, it should reset to 0.
LED Behavior: The LEDs should light up in sequence based on the units digit of the displayed number:
- If the units digit is 0-2, only led1 should be on.
- If the units digit is 3-5, only led2 should be on.
- If the units digit is 6-9, only led3 should be on.
Servo Behavior: The servos should rotate to angles based on the tens digit of the displayed number:
- If the tens digit is 0-2, servo1 should rotate to 30 degrees, servo2 to 60 degrees, and servo3 to 90 degrees.
- If the tens digit is 3-5, servo1 should rotate to 60 degrees, servo2 to 90 degrees, and servo3 to 120 degrees.
- If the tens digit is 6-9, servo1 should rotate to 90 degrees, servo2 to 120 degrees, and servo3 to 150 degrees.
Display Update: The 7-segment displays should update immediately to reflect the new number after each increment.

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
    servo3 = get_servo_value(args["servo3"], driver)
    sevseg1_value = get_sevseg_value(args["sevseg1"],driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"],driver)
    led1_value = get_led_value(args["led1"],driver)
    led2_value = get_led_value(args["led2"],driver)
    led3_value = get_led_value(args["led3"],driver)

    currect = [servo1,servo2,servo3,led1_value,led2_value,led3_value,*sevseg1_value,*sevseg2_value]


    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)

    sev_num = (cur_time//2)%100
    tens = sev_num//10
    ones = sev_num%10
    if ones <= 2:
        co_led = [1,0,0]
    elif ones <=5:
        co_led = [0,1,0]
    else:
        co_led = [0,0,1]

    if tens <= 2:
        co_servo = [30,60,90]
    elif tens <=5:
        co_servo = [60,90,120]
    else:
        co_servo = [90,120,150]

    correct = [*co_servo, *co_led, *sevseg_value[str(tens)], *sevseg_value[str(ones)]]

    return np.allclose(currect, correct, deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(2.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)
    
    correct_sleep(6.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(10.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(14.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(18.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res