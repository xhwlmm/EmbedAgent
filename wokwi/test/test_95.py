'''

**Task**:
You are tasked with programming an Arduino (uno) to control two individual LEDs (led1, led2) and a 10-segment LED bar graph (bargraph1). The LEDs and the bar graph will simulate a loading animation, where the bar graph fills up sequentially, and the individual LEDs blink alternately to indicate activity.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs (led1, led2) and the bar graph (bargraph1) should be off.
Loading Animation:
1. The bar graph (bargraph1) should light up one segment at a time, starting from the first segment (A1) to the last segment (A10).(Pin A1-A10) Each segment should remain lit for 2000 milliseconds before moving to the next segment.
2. While the bar graph is filling up, the two individual LEDs (led1, led2) should blink alternately every 2000 milliseconds. When one LED is on, the other should be off, and vice versa.
3. After the bar graph is fully lit (all 10 segments are on), the bar graph should reset to off, and the animation should restart from the beginning.
4. The entire animation should loop indefinitely.

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
    bargraph_value = get_bargraph_value(args["bargraph1"],driver)

    current = [led1_value, led2_value, *bargraph_value]

    cur_time = get_clock(clock.text)
    cur_time = int(cur_time)
    if (cur_time//2)%2 == 0:
        correct = [1,0] + [1]*((1+cur_time//2)%11) + [0]*(10-(1+cur_time//2)%11)
    else:
        correct = [0,1] + [1]*((1+cur_time//2)%11) + [0]*(10-(1+cur_time//2)%11)


    return np.allclose(current, correct, deviation)
          
def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init
    for _ in range(5):
        correct_sleep(_*2+2.2, clock)
        res["msg"].append(1 if test(clock, driver, args) else 0)




    return res