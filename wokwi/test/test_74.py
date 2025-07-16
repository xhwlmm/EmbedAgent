'''

**Task**:
You are tasked with programming an Arduino (uno) to control two servo motors (servo1, servo2) and a 10-segment LED bar graph (bargraph1) using a push button (btn1). The servos will alternate between three distinct positions, while the LED bar graph will visually indicate the current state. Each button press will advance the system to the next state.

**Detail Rules**:
Initialization:  
- Both servos (servo1, servo2) start at 0° position.  
- All segments of the LED bar graph (bargraph1) remain off.  

State Transitions:  
1. **State 0** (Initial):  
   - Servo1 at 0°, Servo2 at 180°.  
   - All LEDs off.  
   - Maintained for **2 seconds** after initialization.  

2. **State 1** (First button press):  
   - Servo1 at 90°, Servo2 at 90°.  
   - First 5 LEDs of the bar graph lit.  
   - Maintained for **2 seconds**.  

3. **State 2** (Second button press):  
   - Servo1 at 180°, Servo2 at 0°.  
   - All 10 LEDs of the bar graph lit.  
   - Maintained for **2 seconds**.  

4. **State 0** (Third button press):  
   - Returns to initial configuration, repeating the cycle.  

Button Interaction:  
- Each valid button press (debounced for 0.15 seconds) advances the system to the next state.  
- State transitions are locked for **2 seconds** after each button press to ensure stability.  
- The LED bar graph and servo positions must update immediately after a valid state transition.  

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

def test(clock, driver, args, click_num, deviation = 0.2):
    bargraph_1 = get_bargraph_value(args["bargraph1"], driver)
    servo1_value = get_servo_value(args["servo1"], driver)
    servo2_value = get_servo_value(args["servo2"], driver)

    current = [servo1_value, servo2_value, *bargraph_1]
    correct = [90*(click_num%3)]+[180-90*(click_num%3)]+[1]*(click_num%3)*5 + [0] * (2-click_num%3)*5
    return np.allclose(current, correct, atol=deviation)



def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    click_num = 0
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num) else 0)
    time.sleep(2)
    # test 2: click the button
    click_num = 1
    click_button(args['btn1'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num) else 0)
    time.sleep(2)

    # test 3: click the button twice
    click_num = 2
    click_button(args['btn1'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num) else 0)
    time.sleep(2)

    # test 4: click the button three times
    click_num = 3
    click_button(args['btn1'],actions)
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, click_num) else 0)
    
    return res