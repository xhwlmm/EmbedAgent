'''
**Task**:  
You are tasked with programming an Arduino (uno) to control an LED (led1) in a specific on-off sequence.  

**Detail Rules**:  
Initialization: Upon powering on or resetting, the LED should be off.  
Operation Sequence: The LED should follow a repeating cycle of on and off states with specific durations:  
1. First, the LED should turn on and remain lit for 1 second.  
2. Then, the LED should turn off and remain off for 2 seconds.  
3. Next, the LED should turn on again and remain lit for 3 seconds.  
4. Finally, the LED should turn off and remain off for 3 seconds.  
This sequence should repeat indefinitely.
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
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from untils import wait_for_element,move_pot

def test_func(driver, clock, args, res):
    # test 1: in 0.5s led1 should be on
    time.sleep(0.5)
    led1_brightness = args['led1'].get_attribute('brightness')
    if float(led1_brightness) > 0.5:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 2: in 2.5s led1 should be off
    time.sleep(2)
    led1_brightness = args['led1'].get_attribute('brightness')
    if float(led1_brightness) < 0.5:
        res['msg'].append(1)
    else:
        res['msg'].append(0)
    # test 3: in 4.5s led1 should be on
    time.sleep(2)
    led1_brightness = args['led1'].get_attribute('brightness')
    if float(led1_brightness) > 0.5:
        res['msg'].append(1)
    else:
        res['msg'].append(0)

    return res

if __name__ == "__main__":
    pass