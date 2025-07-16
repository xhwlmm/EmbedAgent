'''

**Task**:
You are tasked with programming an Arduino (uno) to create a synchronized display system using an RGB LED (rgb1), a 7-segment display (sevseg1), a shift register (sr1), and a 10-segment LED bar graph (bargraph1). The system will cycle through numbers 0 to 9, updating all components every 2 seconds. The RGB LED will indicate color ranges, the 7-segment display will show the current number, and the LED bar graph will visualize the count.

**Detail Rules**:
1. **Initialization**:  
   - The 7-segment display (sevseg1) shows "0".  
   - The LED bar graph (bargraph1) has all segments off.  
   - The RGB LED (rgb1) is set to red.  

2. **Cycling Behavior**:  
   - Every 2 seconds, increment the displayed number by 1.  
   - After reaching 9, reset to 0 and repeat.  

3. **Component Synchronization**:  
   - The 7-segment display (sevseg1) must show the current number (0-9).  
   - The LED bar graph (bargraph1) must light up a number of segments equal to the current number (e.g., 5 segments for number 5). (from pin:A1 to pin:A10)
   - The RGB LED (rgb1) must follow this color scheme:  
     - **Red** for numbers 0-3  
     - **Green** for numbers 4-6  
     - **Blue** for numbers 7-9  

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,get_sevseg_value,correct_sleep
from untils import sevseg_value

def test(clock, driver, args, deviation=0.2):
   colors = [
       [1,0,0],
       [0,1,0],
       [0,0,1]
   ]
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)

   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   cur_index = (cur_time // 2)
   if cur_index%10 <= 3:
       correct = colors[0]
   elif cur_index%10 <= 6:
       correct = colors[1]
   else:
       correct = colors[2]
   correct += sevseg_value[str(cur_index%10)]
   
   correct += [1]*(cur_index%10)+[0]*(10-cur_index%10)
   current = [*rgb1_value,*sevseg1_value,*bargraph1_value]
   return np.allclose(current, correct, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.3, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.3, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(12.3, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(22.3, clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res
