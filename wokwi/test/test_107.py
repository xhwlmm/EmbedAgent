'''
  
**Task**:  
You are tasked with programming an Arduino (uno) to synchronize a 7-segment display (sevseg1), two LEDs (led1, led2), and a 10-segment LED bar graph (bargraph1) using a shift register (sr1). The system will cycle through numbers 0–9, with the 7-segment display showing the current number, the bar graph indicating the number of active segments, and the LEDs signaling parity (even/odd).  

**Detail Rules**:  
1. **Initialization**:  
   - The 7-segment display (sevseg1) starts at "0".  
   - The bar graph (bargraph1) is fully off.  
   - Both LEDs (led1, led2) are off.  

2. **Cycle Behavior**:  
   - Every 2 seconds, increment the displayed number from 0 to 9. After 9, reset to 0.  
   - The 7-segment display (sevseg1) must show the current number.  
   - The bar graph (bargraph1) lights up segments equal to the current number (e.g., 3 → PIN A1-A3).  
   - **LED Rules**:  
     - If the number is **even**, turn on led1 and turn off led2.  
     - If the number is **odd**, turn on led2 and turn off led1.  

3. **Timing**:  
   - Each number must be displayed for **exactly 2 seconds** before incrementing.  
   - All components must update simultaneously when the number changes.  

4. **Hardware Usage**:  
   - The shift register (sr1) must drive the 7-segment display (sevseg1).  
   - The bar graph (bargraph1) must use direct GPIO pins for segment control.  
   - Both LEDs (led1, led2) must be used to indicate parity.  

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
    sevseg1_value = get_sevseg_value(args["sevseg1"],driver)
    bar1_value = get_bargraph_value(args["bargraph1"],driver)
    led1_value = get_led_value(args['led1'],driver)
    led2_value = get_led_value(args['led2'],driver)

    current = [led1_value,led2_value,*bar1_value,*sevseg1_value]

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    num = (cur_time//2)%10
    if num%2 == 0:
        co_led = [1,0]
    else:
        co_led = [0,1]

    correct = co_led + [1]*(num) + [0]*(9-num) +[0] + sevseg_value[str(num)] 


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

    correct_sleep(18.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res