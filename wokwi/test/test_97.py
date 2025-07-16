'''

**Task**:
You are tasked with programming an Arduino (uno) to create a synchronized visual and mechanical system using three LEDs (led1, led2, led3), three servo motors (servo1, servo2, servo3), and an LED bar graph (bargraph1). The system must cycle through distinct states where servo positions, LED statuses, and bar graph patterns change in sequence.

**Detail Rules**:
1. **Initialization**:  
   - All servos start at 0° position.  
   - All LEDs and bar graph segments remain off.  
   - This state must persist for 2 seconds.  

2. **State Sequence**:  
   - **State 1** (2 seconds):  
     - Servo1 (servo1) moves to 60°.  
     - LED1 (led1) turns on.  
     - First two segments of the bar graph (bargraph1) light up. (PIN A1-A2) 
   - **State 2** (2 seconds):  
     - Servo2 (servo2) moves to 120°.  
     - LED2 (led2) turns on.  
     - Next three segments of the bar graph light up.  (PIN A3-A5) 
   - **State 3** (2 seconds):  
     - Servo3 (servo3) moves to 180°.  
     - LED3 (led3) turns on.  
     - Final three segments of the bar graph light up.  (PIN A6-A8) 
   - **Reset** (2 seconds):  
     - All servos return to 0°.  
     - All LEDs and bar graph segments turn off.  (PIN A1-A8) 
   - The sequence repeats indefinitely after the reset phase.  

3. **Synchronization**:  
   - Servo movements, LED status changes, and bar graph updates must occur simultaneously at the start of each state.  
   - Transitions between states must not overlap; each state must maintain its configuration for at least 2 seconds.  

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



def test(clock, driver, args, deviation=0.2):

    led1_value = get_led_value(args['led1'],driver)
    led2_value = get_led_value(args['led2'],driver)
    led3_value = get_led_value(args['led3'],driver)
    servo1_value = get_servo_value(args["servo1"], driver)
    servo2_value = get_servo_value(args["servo2"], driver)
    servo3_value = get_servo_value(args["servo3"], driver)
    bar1_value = get_bargraph_value(args["bargraph1"], driver)

    current = [led1_value, led2_value, led3_value, servo1_value, servo2_value, servo3_value, *bar1_value]
    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    if (cur_time//2)%4 == 0:
        correct = [0,0,0,0,0,0] + [0,0,0,0,0,0,0,0,0,0]
    elif (cur_time//2)%4 == 1:
        correct = [1,0,0,60,0,0] + [1,1,0,0,0,0,0,0,0,0]
    elif (cur_time//2)%4 == 2:
        correct = [1,1,0,60,120,0] + [1,1,1,1,1,0,0,0,0,0]
    elif (cur_time//2)%4 == 3:
        correct = [1,1,1,60,120,180] + [1,1,1,1,1,1,1,1,0,0]

    return np.allclose(current, correct, deviation)
          
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    correct_sleep(2.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(6.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(10.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    correct_sleep(14.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res