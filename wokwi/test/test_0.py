'''
**Task**:
You are tasked with programming an Arduino (uno) to create an interactive game using three LEDs (led_red, led_yellow, led_green), three pushbuttons (btn_stop, btn_back, btn_forward), and a 7-segment display (sevseg1). The game involves reacting to the LEDs by pressing the correct button within a time limit to score points.

**Detail Rules**:
Initialization: Upon powering on or resetting, all LEDs should be turned off, and the 7-segment display should show "0" to indicate the initial score.

Preparation Phase: Wait for 3 seconds, during which all LEDs remain off, the 7-segment display shows "0", and the serial monitor outputs "Ready Go!". After this, one of the LEDs (red, yellow, or green) will randomly light up.

Game Phase:
1. **Red LED (led_red)**: The red LED will stay lit for 5 seconds. The player must press the "Stop" button (btn_stop) within this time. If the correct button is pressed, the serial monitor will output "Good Job! xN" (where N is the current score, starting at 0 and incrementing by 1 for each correct response), and the game will proceed to the next round. If the wrong button is pressed, the serial monitor will output "Come On!", and the player can try again within the remaining time. If no button is pressed within 5 seconds, the serial monitor will output "Time's up!", and the game will proceed to the next round.

2. **Yellow LED (led_yellow)**: The yellow LED will stay lit for 5 seconds. The player must press the "Back" button (btn_back) within this time. The same rules as the red LED apply for correct, incorrect, or no button presses.

3. **Green LED (led_green)**: The green LED will stay lit for 5 seconds. The player must press the "Forward" button (btn_forward) within this time. The same rules as the red LED apply for correct, incorrect, or no button presses.

Game Repetition: The game will repeat for a total of 5 rounds, with each round having a 2-second interval between LED activations. During these 5 rounds, each LED (red, yellow, and green) must light up at least once.

Game End: After 5 rounds, all LEDs will turn off, and the 7-segment display will show the final score. The serial monitor will output "Game Over! Your score is N", where N is the final score.
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
from untils import wait_for_element,move_pot,get_rgb_value,get_led_value,sevseg_value,get_sevseg_value,get_bargraph_value, random_wait, click_button, get_clock

def test_func(driver, clock, args, res):
    actions = ActionChains(driver)
    serial = wait_for_element('notranslate','class',driver)
    # test 1: init
    time.sleep(3)
    led_red = get_led_value(args['led_red'], driver) > 0.5
    led_yellow = get_led_value(args['led_yellow'], driver) > 0.5
    led_green = get_led_value(args['led_green'], driver) > 0.5
    sevseg1_value = np.array(get_sevseg_value(args['sevseg1'], driver))
    if led_red + led_green + led_yellow == 1 and np.allclose(sevseg1_value,sevseg_value['0'],0.2) and serial.text == 'Ready Go!':
        res["msg"].append(1)
    else:
        res["msg"].append(0)

    # test 2: correct
    btns = ['btn_stop','btn_back','btn_forward']
    for index,i in enumerate([led_red, led_yellow, led_green]):
        if i:
            click_button(args[btns[index]], actions)
            break
    random_wait()
    led_red = get_led_value(args['led_red'], driver) > 0.5
    led_yellow = get_led_value(args['led_yellow'], driver) > 0.5
    led_green = get_led_value(args['led_green'], driver) > 0.5
    sevseg1_value = np.array(get_sevseg_value(args['sevseg1'], driver))
    if led_red + led_green + led_yellow == 0 and np.allclose(sevseg1_value,sevseg_value['1'],0.2) and serial.text == 'Ready Go!\nGood Job! x1':
        res["msg"].append(1)
    else:
        res["msg"].append(0)
    # test 3: time out
    time.sleep(7)
    if serial.text == 'Ready Go!\nGood Job! x1\nTime\'s up!':
        res["msg"].append(1)
    else:
        res["msg"].append(0)
    time.sleep(2)
    # test 4: come on

    led_red = get_led_value(args['led_red'], driver) > 0.5
    led_yellow = get_led_value(args['led_yellow'], driver) > 0.5
    led_green = get_led_value(args['led_green'], driver) > 0.5


    for index,i in enumerate([led_red, led_yellow, led_green]):
        if not i:
            click_button(args[btns[index]], actions)
            time.sleep(0.5)
    for index,i in enumerate([led_red, led_yellow, led_green]):
        if i:
            click_button(args[btns[index]], actions)
            break
    time.sleep(1)
    sevseg1_value = np.array(get_sevseg_value(args['sevseg1'], driver))
    led_red = get_led_value(args['led_red'], driver) > 0.5
    led_yellow = get_led_value(args['led_yellow'], driver) > 0.5
    led_green = get_led_value(args['led_green'], driver) > 0.5
    time.sleep(1)

    if led_red + led_green + led_yellow == 0 and np.allclose(sevseg1_value,sevseg_value['2'],0.2) and serial.text == 'Ready Go!\nGood Job! x1\nTime\'s up!\nCome On!\nCome On!\nGood Job! x2':
        res["msg"].append(1)
    else:
        res["msg"].append(0)
    
    time.sleep(3)
    # test 5: final score
    led_red = get_led_value(args['led_red'], driver) > 0.5
    led_yellow = get_led_value(args['led_yellow'], driver) > 0.5
    led_green = get_led_value(args['led_green'], driver) > 0.5
    for index,i in enumerate([led_red, led_yellow, led_green]):
        if i:
            click_button(args[btns[index]], actions)
            break
    time.sleep(3)
    led_red = get_led_value(args['led_red'], driver) > 0.5
    led_yellow = get_led_value(args['led_yellow'], driver) > 0.5
    led_green = get_led_value(args['led_green'], driver) > 0.5
    for index,i in enumerate([led_red, led_yellow, led_green]):
        if i:
            click_button(args[btns[index]], actions)
            break
    time.sleep(3)
    sevseg1_value = np.array(get_sevseg_value(args['sevseg1'], driver))
    if np.allclose(sevseg1_value,sevseg_value['4'],0.2) and serial.text == 'Ready Go!\nGood Job! x1\nTime\'s up!\nCome On!\nCome On!\nGood Job! x2\nGood Job! x3\nGood Job! x4\nGame Over! Your score is 4':
        res["msg"].append(1)
    else:
        res["msg"].append(0)
    

    return res