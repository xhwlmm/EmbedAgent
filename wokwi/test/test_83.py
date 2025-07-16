'''

**Task**:
You are tasked with programming an Arduino (uno) to control two servos (servo1, servo2) and an RGB LED (rgb1) using two push buttons (btn1, btn2). The RGB LED will display different colors based on the state of the servos, and the push buttons will control the movement of the servos. Specifically:
- Pressing btn1 will rotate servo1 to 90 degrees and change the RGB LED to red.
- Pressing btn2 will rotate servo2 to 180 degrees and change the RGB LED to blue.
- If both buttons are pressed simultaneously, both servos will return to their initial positions (0 degrees), and the RGB LED will turn green.

**Detail Rules**:
Initialization: Upon powering on or resetting, both servos (servo1, servo2) should be at 0 degrees, and the RGB LED (rgb1) should be off.
Button Interaction:
1. When btn1 is pressed:
   - Servo1 (servo1) should rotate to 90 degrees.
   - The RGB LED (rgb1) should turn red.
   - This state should be maintained for at least 2 seconds.
2. When btn2 is pressed:
   - Servo2 (servo2) should rotate to 180 degrees.
   - The RGB LED (rgb1) should turn blue.
   - This state should be maintained for at least 2 seconds.
3. When one button is pressed and another button has already been pressed:
   - Both servos (servo1, servo2) should return to 0 degrees.
   - The RGB LED (rgb1) should turn green.
   - Both buttons return to their unpressed state
   - This state should be maintained for at least 2 seconds.
4. If no buttons are pressed, the RGB LED (rgb1) should remain off, and the servos should stay in their current positions.

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

def int_rgb(args):
   ls = [(1 if i>=0.5 else 0) for i in get_rgb_value(args)]
   return tuple(ls)

def test(clock, driver, args, btn_num, deviation = 0.2):
   servo1_value = get_servo_value(args["servo1"], driver)
   servo2_value = get_servo_value(args["servo2"], driver)
   rgb1_value = get_rgb_value(args["rgb1"], driver)

   current = [servo1_value, servo2_value, *rgb1_value]
   if btn_num == [0,0]:
      correct = [0,0,0,0,0]
   elif btn_num == [1,0]:
      correct = [90,0,1,0,0]
   elif btn_num == [0,1]:
      correct = [0,180,0,0,1]
   elif btn_num == [1,1]:
      correct = [0,0,0,1,0]


   return np.allclose(current, correct, deviation)



def test_func(driver, clock, args, res):
   actions = ActionChains(driver)
   # test 1: init 
   time.sleep(1)
   bnt_num = [0,0]
   res["msg"].append(1 if test(clock, driver, args, bnt_num) else 0)

   # test 2: click the button1 
   bnt_num = [1,0]
   click_button(args['btn1'], actions)
   time.sleep(2)
   res["msg"].append(1 if test(clock, driver, args, bnt_num) else 0)

   # test 3: click the button2 
   bnt_num = [1,1]
   click_button(args['btn2'], actions)
   time.sleep(2)
   res["msg"].append(1 if test(clock, driver, args, bnt_num) else 0)

   # test 2: click the button1 and button2
   bnt_num = [0,1]
   click_button(args['btn2'], actions)
   time.sleep(2)
   res["msg"].append(1 if test(clock, driver, args, bnt_num) else 0)

   return res