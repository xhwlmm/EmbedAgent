'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1) using a shift register (sr1), two servos (servo1, servo2), and three push buttons (btn1, btn2, btn3). The 7-segment display will show a number between 0 and 9, and the servos will rotate to specific angles based on the displayed number. Each push button will increment the displayed number by 1, 2, or 3, respectively. If the number exceeds 9, it should reset to 0.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment display should show "0", and both servos should be at their 0-degree position.
Button Interaction:
1. Pressing btn1 increments the displayed number by 1.
2. Pressing btn2 increments the displayed number by 2.
3. Pressing btn3 increments the displayed number by 3.
Reset Condition: If the number exceeds 9 after incrementing, it should reset to 0.
Servo Control: The servos should rotate to specific angles based on the displayed number:
- For numbers 0-4: servo1 rotates to 0 degrees, and servo2 rotates to 90 degrees.
- For numbers 5-9: servo1 rotates to 90 degrees, and servo2 rotates to 180 degrees.
Display Update: The 7-segment display should immediately update to reflect the new number after each button press.
Servo Update: The servos should immediately rotate to their new positions after the number is updated.

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

    if num<=4:
        correct = [0, 90] + sevseg_value[str(num)]
    else:
        correct = [90, 180] + sevseg_value[str(num)]

    return np.allclose(current, correct, atol=deviation)



def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    time.sleep(1)
    # test 1: init
    click1_num = 0
    click2_num = 0
    click3_num = 0
    prenum = 0
    num = (click1_num + click2_num*2 + click3_num*3)%10
    res["msg"].append(1 if test(clock, driver, args, num, deviation=0.2) else 0)
    # test 2: click the button1
    click1_num = 1
    click2_num = 0
    click3_num = 0
    prenum = num
    num = (click1_num + click2_num*2 + click3_num*3)%10
    if num<prenum:
        num = 0
    click_button(args['btn1'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, num, deviation=0.2) else 0)

    # test 3: click the button2
    click1_num = 1
    click2_num = 1
    click3_num = 0
    prenum = num
    num = (click1_num + click2_num*2 + click3_num*3)%10
    if num<prenum:
        num = 0
    click_button(args['btn2'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, num, deviation=0.2) else 0)

    # test 4: click the button3
    click1_num = 1
    click2_num = 1
    click3_num = 1
    prenum = num
    num = (click1_num + click2_num*2 + click3_num*3)%10
    if num<prenum:
        num = 0
    click_button(args['btn3'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, num, deviation=0.2) else 0)

    # test 5: If the number exceeds 9 after incrementing, it should reset to 0.
    click1_num = 1
    click2_num = 1
    click3_num = 3
    prenum = num
    num = (click1_num + click2_num*2 + click3_num*3)%10
    if num<prenum:
        num = 0
    click_button(args['btn3'],actions)
    time.sleep(0.5)
    click_button(args['btn3'],actions)
    time.sleep(1)
    res["msg"].append(1 if test(clock, driver, args, num, deviation=0.2) else 0)
    
    return res