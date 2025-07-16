'''

**Task**:
You are tasked with programming an Arduino (uno) to control a 7-segment display (sevseg1), a 10-segment LED bar graph (bargraph1), and three slide potentiometers (pot1, pot2, pot3). The 7-segment display will show a single digit (0-9), and the LED bar graph will light up a number of segments corresponding to the digit displayed. The slide potentiometers will control the brightness of the LED bar graph and the speed at which the digit changes.

**Detail Rules**:
1. **7-Segment Display (sevseg1)**:
   - The display will show a single digit (0-9).
   - The digit will increment by 1 every 2 seconds, looping back to 0 after 9.

2. **LED Bar Graph (bargraph1)**:
   - The number of lit segments on the bar graph will correspond to the digit displayed on the 7-segment display. For example, if the digit is 3, 3 segments will light up.
   - The brightness of the lit segments will be controlled by the first potentiometer (pot1). The brightness value will range from 0 (off) to 255 (maximum brightness).

3. **Slide Potentiometers**:
   - The first potentiometer (pot1) will control the brightness of the LED bar graph.
   - The third potentiometer (pot2) will control the speed at which the digit on the 7-segment display changes. The speed will range from 1 second to 2 seconds.
   - The third potentiometer (pot3) will control the speed at which the digit on the 7-segment display changes. The speed will range from 1 second to 2 seconds.
   - The final speed will be the sum of the values from pot2 and pot3.

4. **State Maintenance**:
   - The system should continuously update based on the current values of the potentiometers.

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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value, get_clock, get_servo_value,get_sevseg_value, get_bargraph_value
from untils import sevseg_value,correct_sleep

def test_func(driver, clock, args, res): 
   deviation=0.2
   # test 1 
   time.sleep(0.3)
   move_pot(args['pot1'],1,driver)
   correct_sleep(4.2, clock)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   bar1_value = get_bargraph_value(args['bargraph1'], driver)
   correct_pot1_value = [1]*2+[0]*8
   if np.allclose(sevseg1_value,sevseg_value['2'],rtol=deviation) and np.allclose(bar1_value,correct_pot1_value,rtol=deviation):
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   # test 2
   move_pot(args['pot2'],1,driver)
   time.sleep(0.5)
   move_pot(args['pot3'],1,driver)
   time.sleep(0.5)
   correct_sleep(12.2, clock)
   sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   correct_sleep(16.2, clock)
   new_sevseg1_value = get_sevseg_value(args['sevseg1'], driver)
   for num in sevseg_value:
      if np.allclose(sevseg1_value,sevseg_value[num],rtol=deviation):
         sevseg1_num = int(num)
      if np.allclose(new_sevseg1_value,sevseg_value[num],rtol=deviation):
         new_sevseg1_num = int(num)
   bar1_value = get_bargraph_value(args['bargraph1'], driver)
   correct_bar1_value = [1 if i<new_sevseg1_num else 0 for i in range(10)]
   if new_sevseg1_num - sevseg1_num == 1 and np.allclose(bar1_value,correct_bar1_value,rtol=deviation):
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   # test 3
   move_pot(args['pot1'],0,driver)
   time.sleep(0.8)
   correct_bar1_value = [0 for i in range(10)]
   bar1_value = get_bargraph_value(args['bargraph1'], driver)
   if np.allclose(bar1_value,correct_bar1_value,rtol=deviation):
      res['msg'].append(1)
   else:
      res['msg'].append(0)
   return res

