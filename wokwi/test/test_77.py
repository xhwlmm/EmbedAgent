'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) using a shift register (sr1), two servo motors (servo1, servo2), and a push button (btn1). The 7-segment display will show a number that increments by 1 each time the button is pressed. Simultaneously, the two servo motors will rotate to specific angles based on the displayed number. The servos should move to 0° when the number is even and to 90° when the number is odd.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should show "0", and both servo motors (servo1, servo2) should be at 0°.
Button Interaction: Each press of the button (btn1) should increment the displayed number by 1. The number should be displayed on the 7-segment display (sevseg1).
Servo Movement: After each button press, the two servo motors (servo1, servo2) should move to 0° if the displayed number is even or to 90° if the displayed number is odd.
Reset Condition: If the number exceeds 9 after incrementing, it should reset to 0.
Display Update: The 7-segment display should immediately update to reflect the new number after each button press.
Servo Update: The servo motors should move to their new positions immediately after the number is updated.

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

def test(clock, driver, args, num, deviation=0.2):
    servo1 = get_servo_value(args["servo1"], driver)
    servo2 = get_servo_value(args["servo2"], driver)
    sevseg1_value = get_sevseg_value(args["sevseg1"], driver)


    current = [servo1, servo2, *sevseg1_value]
    if num % 2 == 0:
        correct = [0, 0, *sevseg_value[str(num)]]
    else:
        correct = [90, 90, *sevseg_value[str(num)]]

    return np.allclose(current, correct, atol=deviation)



def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    click_button(args['btn1'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, 1, deviation=0.2) else 0)
    # test 2: click the button1
    click_button(args['btn1'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, 2, deviation=0.2) else 0)

    # test 3: click the button2
    click_button(args['btn1'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, 3, deviation=0.2) else 0)
    
    return res