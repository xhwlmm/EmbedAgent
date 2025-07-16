'''

**Task**:
You are tasked with programming an Arduino (uno) to control a servo motor (servo1) and a LED bar graph (bargraph1) using three push buttons (btn1, btn2, btn3). The servo motor will rotate to specific angles based on the button pressed, and the LED bar graph will visually indicate the current angle of the servo motor. Each button corresponds to a specific angle, and the LED bar graph will light up proportionally to the angle.

**Detail Rules**:
Initialization: Upon powering on or resetting, the servo motor (servo1) should be at 0 degrees, and the LED bar graph (bargraph1) should be off.
Button Interaction:
1. When btn1 is pressed, the servo motor (servo1) should rotate to 30 degrees. The LED bar graph (bargraph1) should light up the first 3 LEDs to indicate the angle.
2. When btn2 is pressed, the servo motor (servo1) should rotate to 60 degrees. The LED bar graph (bargraph1) should light up the first 6 LEDs to indicate the angle.
3. When btn3 is pressed, the servo motor (servo1) should rotate to 90 degrees. The LED bar graph (bargraph1) should light up all 10 LEDs to indicate the angle.
State Maintenance: Each state (angle and corresponding LED bar graph display) should be maintained for at least 2 seconds to allow for verification.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,get_bargraph_value,click_button,get_servo_value

def test(clock, driver, args, btn_num, deviation=0.2):
    correct = []
    if btn_num == 0:
        correct = [0]*10+[0]
    elif btn_num == 1:
        correct = [1]*3+[0]*7+[30]
    elif btn_num == 2:
        correct = [1]*6+[0]*4+[60]
    elif btn_num == 3:
        correct = [1]*10+[90]
    bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
    servo1_value = get_servo_value(args['servo1'], driver)
    current = [*bargraph1_value, servo1_value]
    return np.allclose(current, correct, atol=deviation)
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_num = 0
    res["msg"].append(1 if test(clock, driver, args, btn_num) else 0)
    # test 2: click the button
    btn_num = 1
    click_button(args['btn1'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_num) else 0)

    # test 3: click the button twice
    btn_num = 3
    click_button(args['btn3'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_num) else 0)

    # test 4: click the button three times
    btn_num = 2
    click_button(args['btn2'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_num) else 0)
    
    return res