'''

**Task**:
You are tasked with programming an Arduino (uno) to control two servos (servo1, servo2) and an LED (led1) using two push buttons (btn1, btn2). The servos will rotate to specific angles based on the button presses, and the LED will indicate the state of the system. The system should behave as follows:
- Pressing btn1 will rotate servo1 to 90 degrees and turn on the LED.
- Pressing btn2 will rotate servo2 to 180 degrees and turn off the LED.
- -If one button has already been pressed and the other button is pressed, both servo systems will return to their initial position (0 degrees) and the LED will flash at a frequency of 0.25 Hz. (2 second on, one 2 off)

**Detail Rules**:
Initialization: Upon powering on or resetting, both servos should be at 0 degrees, and the LED should be off.
Button Interaction:
1. Pressing btn1 will rotate servo1 to 90 degrees and turn on the LED. This state should be maintained for at least 2 seconds.
2. Pressing btn2 will rotate servo2 to 180 degrees and turn off the LED. This state should be maintained for at least 2 seconds.
3. If one button has already been pressed and the other button is pressed, both servo systems will return to 0 degrees and the LED will flash at a frequency of 025 Hz (on for 2 second, off for 2 second). This state should be maintained until btn1 or btn2 is pressed again.
State Maintenance: Each state (servo angles and LED state) should be maintained for at least 2 seconds to allow for verification.

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



def test(clock, driver, args, btn_click, deviation=0.2):

    led1 = get_led_value(args['led1'],driver)

    servo1 = get_servo_value(args['servo1'],driver)
    servo2 = get_servo_value(args['servo2'],driver)

    current = [led1,servo1,servo2]

    if btn_click == [0,0]:
        correct = [0,0,0]
    elif btn_click == [1,0]:
        correct = [1,90,0]
    elif btn_click == [0,1]:
        correct = [0,0,180]
    elif btn_click == [1,1]:
        return np.allclose([1,servo1,servo2],[1,0,0],deviation)
    else:
        return 0
    
    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_click = [0,0]
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    btn_click = [1,0]
    last_click = 1
    click_button(args['btn1'], actions)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)

    btn_click = [1,1]
    last_click = 2
    click_button(args['btn2'], actions)
    time.sleep(2.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click) else 0)


    return res