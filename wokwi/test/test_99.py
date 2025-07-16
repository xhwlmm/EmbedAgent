'''
  
**Task**:  
You are tasked with programming an Arduino (uno) to control an LED (led1) and a 10-segment LED bar graph (bargraph1) using a slide potentiometer (pot1). The potentiometer will adjust the brightness of the LED and dynamically light up segments of the bar graph based on its position.  

**Detail Rules**:  
1. **Initialization**:  
   - On startup, the LED (led1) and all segments of the bar graph (bargraph1) must be off.  

2. **Potentiometer Interaction**:  
   - The slide potentiometer (pot1) controls two behaviors:  
     a. **LED Brightness**: The LED's brightness is directly proportional to the potentiometer's value (0 = off, 1023 = full brightness).  
     b. **Bar Graph Activation**: The bar graph (bargraph1) lights up segments sequentially from 1 to 10, corresponding to the potentiometer's value. For example:  
       - 0-102: 0 segments lit  
       - 103-204: 1 segment lit  (Pin A1)
       - ...  
       - 921-1023: 10 segments lit (Pin A10)

3. **LED Blinking Condition**:  
   - When the potentiometer (pot1) is at its maximum value (1023), the LED (led1) must blink at 0.25 Hz (on for 2 second, off for 2 second) instead of staying fully lit.  

5. **Hardware Usage**:  
   - All components (uno, led1, pot1, bargraph1) must be used as described.  

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



def test(clock, driver, args, correct, deviation=0.2):

   led1_value = get_led_value(args['led1'],driver)
   bar1_value = get_bargraph_value(args["bargraph1"],driver)

   current = [led1_value, *bar1_value]
   return np.allclose(current, correct, atol=deviation)
          
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    time.sleep(1)
    pot_pos = 0
    res["msg"].append(1 if test(clock, driver, args,[0]*11, pot_pos) else 0)

    pot_pos = 1
    move_pot(args['pot1'],pot_pos,driver)
    res["msg"].append(1 if test(clock, driver, args,[1]*11, pot_pos) else 0)

    time.sleep(1)

    pot_pos = 0
    move_pot(args['pot1'],pot_pos,driver)
    time.sleep(0.5)
    driver.save_screenshot('screenshot.png')
    res["msg"].append(1 if test(clock, driver, args,[0]*11 ,pot_pos) else 0)



    return res