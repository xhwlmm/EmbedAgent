'''

**Task**:
You are tasked with programming an Arduino (uno) to control the brightness and behavior of an LED (led1) using two push buttons (btn1, btn2) and three slide potentiometers (pot1, pot2, pot3). The LED's brightness will be controlled by the potentiometers, and the buttons will determine the mode of operation. The system should have two modes: Manual Mode and Auto Mode. In Manual Mode, the LED's brightness is directly controlled by one potentiometer. In Auto Mode, the LED's brightness cycles through a range determined by the other two potentiometers.

**Detail Rules**:
1. **Initialization**: Upon powering on or resetting, the LED (led1) should be off, and the system should start in Manual Mode.
2. **Manual Mode**:
   - The brightness of the LED (led1) is controlled by the value of the first potentiometer (pot1). The value of pot1 is mapped to the LED's brightness (0 to 255).
   - The second potentiometer (pot2) and third potentiometer (pot3) are ignored in this mode.
   - Pressing the first button (btn1) switches the system to Auto Mode.
3. **Auto Mode**:
   - The LED (led1) cycles through a brightness range determined by the second potentiometer (pot2) and third potentiometer (pot3). The minimum brightness is set by pot2, and the maximum brightness is set by pot3.
   - The LED's brightness smoothly transitions between the minimum and maximum values, with each transition taking 2 seconds.
   - Pressing the second button (btn2) switches the system back to Manual Mode.
4. **Button Debouncing**: Both buttons (btn1, btn2) must be debounced to avoid false triggers caused by mechanical vibrations. A debounce delay of 150 milliseconds should be used.
5. **Mode Indication**: The current mode (Manual or Auto) should be indicated by the LED's behavior:
   - In Manual Mode, the LED's brightness is static and directly controlled by pot1.
   - In Auto Mode, the LED's brightness cycles between the minimum and maximum values set by pot2 and pot3.
6. **State Persistence**: Each state (Manual or Auto Mode) should persist for at least 2 seconds before switching to ensure proper verification.

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



def test(clock, driver, args, ledmode, pot_pos, deviation=0.2):

    led1 = get_led_value(args['led1'],driver)


    current = [led1]

    if ledmode == 0:
        correct = [pot_pos[0]]
    else:
        correct = [(pot_pos[1]+pot_pos[2])//2]
    
    return np.allclose(current,correct,deviation)

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    pot_pos = [0,0,0]
    ledmode = 0
    res["msg"].append(1 if test(clock, driver, args, ledmode, pot_pos) else 0)

    pot_pos = [1,0,0]
    ledmode = 0
    move_pot(args['pot1'],1,driver)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, ledmode, pot_pos) else 0)

    pot_pos = [1,1,1]
    ledmode = 1
    move_pot(args['pot2'],1,driver)
    move_pot(args['pot3'],1,driver)
    click_button(args['btn1'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, ledmode, pot_pos) else 0)

    pot_pos = [0,1,1]
    ledmode = 0
    move_pot(args['pot1'],0,driver)
    click_button(args['btn2'], actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, ledmode, pot_pos) else 0)

    return res