'''

**Task**:
You are tasked with programming an Arduino (uno) to control a servo motor (servo1) using three push buttons (btn1, btn2, btn3) and three slide potentiometers (pot1, pot2, pot3). The servo motor's position will be controlled by the potentiometers, and the buttons will determine which potentiometer is active for controlling the servo. Each button corresponds to one potentiometer, and pressing a button will enable the corresponding potentiometer to control the servo's position.

**Detail Rules**:
Initialization: Upon powering on or resetting, the servo motor (servo1) should be at its default position (0 degrees).
Button Interaction:
1. Pressing btn1 will enable pot1 to control the servo's position. The servo's position will be mapped to the value of pot1 (0 to 1023) and set to a corresponding angle between 0 and 180 degrees.
2. Pressing btn2 will enable pot2 to control the servo's position. The servo's position will be mapped to the value of pot2 (0 to 1023) and set to a corresponding angle between 0 and 180 degrees.
3. Pressing btn3 will enable pot3 to control the servo's position. The servo's position will be mapped to the value of pot3 (0 to 1023) and set to a corresponding angle between 0 and 180 degrees.
4. Only one potentiometer can be active at a time. The last button pressed determines which potentiometer is active.

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

def test(btn_cnt, pot_pos, args, driver, deviation=1):
    servo1_value = get_servo_value(args['servo1'],driver)
    if pot_pos[btn_cnt] == 0:
        if abs(servo1_value - 0) < 1:
            return True
        else:
            return False
    else:
        if abs(servo1_value - 180) < 1:
            return True
        else:
            return False
        


def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    btn_cnt = 0
    click_button(args['btn1'], actions)
    move_pot(args['pot1'], 1, driver)
    pot_pos = [1,0,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, pot_pos, args, driver) else 0)
    # test 2: click the button
    btn_cnt+=1
    click_button(args['btn2'], actions)
    pot_pos = [1,0,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, pot_pos, args, driver) else 0)

    # test 3: click the button twice
    move_pot(args['pot2'], 1, driver)
    pot_pos = [1,1,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, pot_pos, args, driver) else 0)

    # test 4: click the button three times
    btn_cnt+=1
    click_button(args['btn3'], actions)
    pot_pos = [1,1,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, pot_pos, args, driver) else 0)

    # test 5: click the button four times
    move_pot(args['pot3'], 1, driver)
    pot_pos = [1,1,1]
    time.sleep(0.5)
    res["msg"].append(1 if test(btn_cnt, pot_pos, args, driver) else 0)
    
    return res