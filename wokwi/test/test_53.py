'''

**Task**:
You are tasked with programming an Arduino (uno) to create a dynamic lighting system using an RGB LED (rgb1), three servo motors (servo1, servo2, servo3), and an LED bar graph (bargraph1). The RGB LED's color and the bar graph's illumination level must be determined by the angular positions of the servos. 

**Detail Rules**:
1. **Initialization**:  
   - All servos start at 0° position.  
   - The RGB LED (rgb1) and bar graph (bargraph1) are initially off.  

2. **Servo Control**:  
   - Servo1 controls the **red** channel of the RGB LED.  
   - Servo2 controls the **green** channel.  
   - Servo3 controls the **blue** channel.  
   - Each servo's angle (0°–180°) maps linearly to its corresponding RGB channel's brightness (0–255).  
   - Every 2 seconds, one servo move 180°, the order is servo1 -> servo2 -> servo3 -> servo1 ... if the servo is at 0°, it will move to 180°, if it is at 180°, it will move to 0°.

3. **LED Bar Graph**:  
   - The bar graph (bargraph1) displays the **average brightness** of the RGB LED.  
   - The average brightness is calculated as `(R + G + B) / 3` and mapped to light 0–8 LEDs on the bar graph. (from pin:A1 to pin:A8)

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_bargraph_value,correct_sleep

def test(clock, driver, args, deviation=0.2):
   colors = [
       [0,0,0],
       [1,0,0],
       [1,1,0],
       [1,1,1],
       [0,1,1],
       [0,0,1],
   ]
   rgb1_value = get_rgb_value(args['rgb1'], driver)
   servo1_value = get_servo_value(args['servo1'],driver)
   servo2_value = get_servo_value(args['servo2'],driver)
   servo3_value = get_servo_value(args['servo3'],driver)
   bargraph1_value = get_bargraph_value(args['bargraph1'], driver)
   cur_time = get_clock(clock.text)
   cur_time = int(cur_time)
   cur_index = (cur_time // 2) % 6
   if colors[cur_index].count(1) == 0:
       correct_bargraph = [0]*10
   elif colors[cur_index].count(1) == 1:
       correct_bargraph = [1]*2 + [0]*8
   elif colors[cur_index].count(1) == 2:
       correct_bargraph = [1]*5 + [0]*5
   elif colors[cur_index].count(1) == 3:
       correct_bargraph = [1]*8 + [0]*2

   correct_color = colors[cur_index]
   correct = [*correct_bargraph,*correct_color,*(np.array(correct_color)*180)]
   
   current = [*bargraph1_value, *rgb1_value, servo1_value, servo2_value, servo3_value]
   return np.allclose(current, correct, atol=deviation)

def test_func(driver, clock, args, res):    
    # test 1
    correct_sleep(2.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 2
    correct_sleep(6.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 3
    correct_sleep(12.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    # test 4
    correct_sleep(22.2,clock)
    res["msg"].append(1 if test(clock, driver, args) else 0)

    return res
