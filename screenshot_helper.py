import pyautogui
from pynput.keyboard import Key, Listener
import os
from datetime import datetime
import time

index = 1
date = str(datetime.today())[:10]


def on_press(key):
    global index
    if key == Key.ctrl_r:
        time.sleep(1)
        pyautogui.scroll(-400)
        time.sleep(1)
        pyautogui.screenshot(f"{date}/{index:03d}.png")
        index += 1
    elif key == "q":
        exit()


if not os.path.isdir(f"./{date}"):
    os.mkdir(f"./{date}")

with Listener(on_press=on_press) as listener:
    listener.join()
