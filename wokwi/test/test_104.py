'''

**Task**:
You are tasked with programming an Arduino (uno) to control two 7-segment displays (sevseg1, sevseg2) using two shift registers (sr1, sr2), two LEDs (led1, led2), and three slide potentiometers (pot1, pot2, pot3). The 7-segment displays will show a two-digit number, where one display represents the tens digit and the other represents the units digit. The potentiometers will control the brightness of the LEDs and the displayed number. The LEDs will indicate whether the displayed number is even or odd.

**Detail Rules**:
Initialization: Upon powering on or resetting, the 7-segment displays should show "00", and both LEDs should be off.
Potentiometer Interaction:
1. The first potentiometer (pot1) controls the brightness of the first LED (led1). The value of pot1 is mapped to a PWM range (0-255) to adjust the LED's brightness.
2. The second potentiometer (pot2) controls the brightness of the second LED (led2). The value of pot2 is mapped to a PWM range (0-255) to adjust the LED's brightness.
3. The third potentiometer (pot3) controls the displayed number on the 7-segment displays. The value of pot3 is mapped to a range of 0-99, with the tens digit displayed on the first 7-segment display (sevseg1) and the units digit displayed on the second 7-segment display (sevseg2).
LED Indication:
1. If the displayed number is even, the first LED (led1) should be on, and the second LED (led2) should be off.
2. If the displayed number is odd, the first LED (led1) should be off, and the second LED (led2) should be on.
Display Update: The 7-segment displays and LEDs should update continuously based on the current values of the potentiometers.

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
    sevseg1_value = get_sevseg_value(args["sevseg1"],driver)
    sevseg2_value = get_sevseg_value(args["sevseg2"],driver)

    led1 = get_led_value(args["led1"],driver)
    led2 = get_led_value(args["led2"],driver)

    current = [led1,led2,*sevseg1_value,*sevseg2_value]

    num = 99*pot_pos[2]
    if num%2 == 0:
        correct = [pot_pos[0],0,*sevseg_value[str(num//10)],*sevseg_value[str(num%10)]]
    else:
        correct = [0,pot_pos[1],*sevseg_value[str(num//10)],*sevseg_value[str(num%10)]]

    return np.allclose(current, correct, deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    pot_pos = [0,0,0]
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    # test 2
    pot_pos = [1,0,0]
    move_pot(args["pot1"],1,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    # test 3
    pot_pos = [1,0,1]
    move_pot(args["pot1"],1,driver)
    move_pot(args["pot2"],0,driver)
    move_pot(args["pot3"],1,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)


    # test 4
    pot_pos = [1,1,1]
    move_pot(args["pot1"],1,driver)
    move_pot(args["pot2"],1,driver)
    move_pot(args["pot3"],1,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, pot_pos) else 0)
    
    return res