'''

**Task**:
You are tasked with programming an Arduino (uno) to control a servo motor (servo1), an LED (led1), and three slide potentiometers (pot1, pot2, pot3). The servo motor's position will be controlled by one potentiometer, the LED's brightness by another, and the third potentiometer will determine the speed at which the servo moves to its target position.

**Detail Rules**:
1. **Servo Control**:
   - The position of the servo motor (servo1) is controlled by the first potentiometer (pot1). The value of pot1 (0 to 1023) is mapped to the servo's angle range (0 to 180 degrees).
   - The servo should move smoothly to the target position determined by pot1.

2. **LED Brightness Control**:
   - The brightness of the LED (led1) is controlled by the second potentiometer (pot2). The value of pot2 (0 to 1023) is mapped to the LED's brightness range (0 to 255).

3. **Servo Speed Control**:
   - The speed at which the servo moves to its target position is controlled by the third potentiometer (pot3). The value of pot3 (0 to 1023) is mapped to a delay range (e.g., 10 to 100 milliseconds) between each step of the servo's movement.

4. **State Maintenance**:
   - The servo's position, LED brightness, and movement speed should update continuously based on the current values of the potentiometers.

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
from untils import sevseg_value,move_pot,get_rgb_value,get_led_value,get_sevseg_value,sevseg_value,get_clock,get_bargraph_value,click_button,get_servo_value


def test(clock, driver, args, pot_pos, deviation=0.2):
    led1_value = get_led_value(args["led1"], driver)
    servo1_value = get_servo_value(args["servo1"], driver)
    current = [led1_value, servo1_value]

    if pot_pos == [0,0,0]:
        return np.allclose(current, [0,0], deviation)

    if pot_pos[2] == 0:
        correct = [pot_pos[1], 180]
    else:
        return np.allclose(led1_value, pot_pos[1] ,deviation) and (servo1_value != 0)

    return np.allclose(current, correct, deviation)
    
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    time.sleep(1)
    pot_pos = [0,0,0]
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)

    # test 2
    pot_pos = [1,1,0]
    move_pot(args["pot3"],0,driver)
    move_pot(args["pot1"],1,driver)
    move_pot(args["pot2"],1,driver)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)

    # test 3
    pot_pos = [0,1,1]
    move_pot(args["pot3"],1,driver)
    move_pot(args["pot1"],0,driver)
    move_pot(args["pot2"],1,driver)
    time.sleep(2)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    return res