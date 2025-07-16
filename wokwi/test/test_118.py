'''

**Task**:
You are tasked with programming an Arduino (uno) to control a servo motor (servo1) and an LED (led1) using two push buttons (btn1, btn2). The servo motor should rotate to specific angles based on the button presses, and the LED should indicate the state of the system. The first button (btn1) will increment the servo angle by 30 degrees, and the second button (btn2) will decrement the servo angle by 30 degrees. The LED should turn on when the servo start moving

**Detail Rules**:
Initialization: Upon powering on or resetting, the servo motor (servo1) should be at 90 degrees, and the LED (led1) should be off.
Button Interaction:
1. When the first button (btn1) is pressed, the servo motor (servo1) should increment its angle by 30 degrees (up to a maximum of 180 degrees). The LED (led1) should turn on while the servo is moving and turn off once the servo reaches the new angle.
2. When the second button (btn2) is pressed, the servo motor (servo1) should decrement its angle by 30 degrees (down to a minimum of 0 degrees). The LED (led1) should turn on while the servo is moving and turn off once the servo reaches the new angle.
3. If the servo is already at the maximum or minimum angle, pressing the corresponding button should have no effect, and the LED (led1) should remain off.
Servo Movement: The servo motor (servo1) should move smoothly to the new angle, and the LED (led1) should remain on for at least 2 seconds during the movement.

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



def test(clock, driver, args, btn1_click, btn2_click, deviation=0.2):

    led1 = get_led_value(args['led1'],driver)

    servo1 = get_servo_value(args['servo1'],driver)

    current = [led1,servo1]

    sv = 90+btn1_click*30-btn2_click*30
    if sv<0:
        sv = 0
    elif sv>180:
        sv = 180

    correct = [1,sv]

    
    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)

    btn1_click = 1
    btn2_click = 0
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn1_click, btn2_click) else 0)
    time.sleep(2)

    btn1_click = 2
    btn2_click = 0
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn1_click, btn2_click) else 0)
    time.sleep(2)

    btn1_click = 2
    btn2_click = 1
    click_button(args['btn2'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn1_click, btn2_click) else 0)


    return res