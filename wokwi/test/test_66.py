'''

**Task**:
You are tasked with programming an Arduino (uno) to control three servo motors (servo1, servo2, servo3) using a push button (btn1). Each press of the button will cycle through a sequence of predefined angles for the servos. The servos should move to their respective angles in the sequence, and each state should be maintained for at least 2 seconds before transitioning to the next state.

**Detail Rules**:
Initialization: Upon powering on or resetting, all servos (servo1, servo2, servo3) should be set to their initial position of 0 degrees.
Button Interaction: Each press of the button (btn1) will advance the system to the next state in the sequence. The sequence of states is as follows:
1. State 1: Servo1 = 0°, Servo2 = 0°, Servo3 = 0°.
2. State 2: Servo1 = 90°, Servo2 = 45°, Servo3 = 135°.
3. State 3: Servo1 = 180°, Servo2 = 90°, Servo3 = 0°.
4. State 4: Servo1 = 45°, Servo2 = 135°, Servo3 = 90°.
5. State 5: Servo1 = 0°, Servo2 = 0°, Servo3 = 0° (reset to initial state).
State Transition: After reaching State 5, the sequence should reset to State 1 on the next button press.
Debouncing: The button press should be debounced to avoid false triggers caused by mechanical vibrations.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,sevseg_value,get_sevseg_value,click_button,get_servo_value

def test(btn_cnt, args, driver, deviation=1):
    servo1_value = get_servo_value(args['servo1'],driver)
    servo2_value = get_servo_value(args['servo2'],driver)
    servo3_value = get_servo_value(args['servo3'],driver)
    btn_cnt = btn_cnt % 5
    current = [servo1_value,servo2_value,servo3_value]
    if btn_cnt == 0:
        return np.allclose(current, [0,0,0], atol=deviation)
    elif btn_cnt == 1:
        return np.allclose(current, [90,45,135], atol=deviation)
    elif btn_cnt == 2:
        return np.allclose(current, [180,90,0], atol=deviation)
    elif btn_cnt == 3:
        return np.allclose(current, [45,135,90], atol=deviation)
    elif btn_cnt == 4:
        return np.allclose(current, [0,0,0], atol=deviation)
        


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_cnt = 1
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, args, driver) else 0)
    # test 2: click the button
    btn_cnt+=1
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, args, driver) else 0)

    # test 3: click the button twice
    btn_cnt+=1
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, args, driver) else 0)

    # test 4: click the button three times
    btn_cnt+=1
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, args, driver) else 0)

    # test 5: click the button four times
    btn_cnt+=1
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, args, driver) else 0)
    
    return res