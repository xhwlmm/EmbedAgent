'''

**Task**:
You are tasked with programming an Arduino (uno) to control three LEDs (led1, led2, led3) using three push buttons (btn1, btn2, btn3) and three slide potentiometers (pot1, pot2, pot3). Each LED corresponds to a specific button and potentiometer. When a button is pressed, the corresponding LED's brightness will be set based on the value of its associated potentiometer. The brightness of each LED should remain stable for at least 2 seconds after a button press to allow for verification.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs (led1, led2, led3) should be off.
Button and Potentiometer Interaction:
1. Each button (btn1, btn2, btn3) is associated with a specific LED (led1, led2, led3) and potentiometer (pot1, pot2, pot3).
2. When a button is pressed, the corresponding LED's brightness should be set to a value proportional to the potentiometer's position. The potentiometer value ranges from 0 to 1023, and the LED brightness should range from 0 to 255.
3. The brightness of the LED should remain stable for at least 2 seconds after the button is pressed.
4. If no button is pressed, the LEDs should maintain their current brightness levels.
5. Each button press should only affect its corresponding LED, leaving the other LEDs unchanged.

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



def test(clock, driver, args, btn_click, pot_pos, deviation=0.2):

    led1 = get_led_value(args['led1'],driver)
    led2 = get_led_value(args['led2'],driver)
    led3 = get_led_value(args['led3'],driver)


    current = [led1,led2,led3]

    correct = [pot_pos[0]*btn_click[0],pot_pos[1]*btn_click[1],pot_pos[2]*btn_click[2]]
    
    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    pot_pos = [0,0,0]
    btn_click = [0,0,0]
    res["msg"].append(1 if test(clock, driver, args, btn_click, pot_pos) else 0)

    pot_pos = [1,1,1]
    btn_click = [1,0,0]
    move_pot(args['pot1'],1,driver)
    move_pot(args['pot2'],1,driver)
    move_pot(args['pot3'],1,driver)
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click, pot_pos) else 0)

    pot_pos = [1,1,1]
    btn_click = [1,1,0]
    click_button(args['btn2'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click, pot_pos) else 0)

    pot_pos = [1,1,1]
    btn_click = [1,1,1]
    click_button(args['btn3'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, btn_click, pot_pos) else 0)

    return res