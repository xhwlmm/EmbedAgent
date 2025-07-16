'''

**Task**:
You are tasked with programming an Arduino (uno) to control an RGB LED (rgb1) and an LED bar graph (bargraph1) using three pushbuttons (btn1, btn2, btn3). Each button adjusts the intensity of a specific color component (red, green, blue) in the RGB LED, while the bar graph visually indicates the current intensity level of the most recently adjusted color.

**Detail Rules**:
1. **Initialization**:  
   - The RGB LED (rgb1) and LED bar graph (bargraph1) must be off when the system starts.  
2. **Button Functionality**:  
   - **btn1**: Increases the red intensity by 32 (0-255 range). After reaching 255, the next press resets to 0.  
   - **btn2**: Adjusts the green intensity in the same manner.  
   - **btn3**: Adjusts the blue intensity in the same manner.  
   - Each button press must update the bar graph to display the current intensity level of the adjusted color, the pins of the bar chart are A1-A8 .(e.g., 32 = 1 LED lit, 64 = 2 LEDs lit, up to 255 = 8 LEDs lit). (the bargraph display the intensity of the light corresponding to the button currently pressed)
3. **RGB LED Behavior**:  
   - The RGB LED must display the combined color based on the current red, green, and blue intensities.  
4. **Stability**:  
   - Button presses must be debounced to avoid false triggers.  

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


def test(clock, driver, args, colors, click_num, deviation = 0.2):
    rgb1_value = get_rgb_value(args["rgb1"],driver)
    bar1_value = get_bargraph_value(args['bargraph1'],driver)

    current = [*rgb1_value, *bar1_value]
    correct = colors + [1]*(click_num%8) + [0]*(10-click_num%8)

    return np.allclose(current, correct, deviation)



def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    # test 1: init 
    time.sleep(1)
    colors = [0,0,0]
    click_num = 0
    time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, colors, click_num) else 0)

    # test 2: click the button1 
    colors = [1,0,0]
    click_num = 7
    for _ in range(7):
        click_button(args['btn1'], actions)
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, colors, click_num) else 0)

    # test 3: click the button2 
    colors = [1,1,0]
    click_num = 7
    for _ in range(7):
        click_button(args['btn2'], actions)
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, colors, click_num) else 0)

    # test 4: 
    colors = [1,1,1]
    click_num = 7
    for _ in range(7):
        click_button(args['btn3'], actions)
        time.sleep(0.5)
    res["msg"].append(1 if test(clock, driver, args, colors, click_num) else 0)



    return res