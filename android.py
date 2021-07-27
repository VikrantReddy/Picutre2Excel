from ppadb.client import Client
import time
from rich.progress import Progress

import cv2
import numpy as np
import sys

adb = Client(host="127.0.0.1", port=5037)
device = adb.devices()[0]


def take_screenshot(device):
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)


folder = cv2.imread("folder.png")

number = int(sys.argv[1])

with Progress() as progress:

    task1 = progress.add_task("[red]Downloading...", total=number)

    for page in range(number//15 or 1):
        for row in range(5):
            for col in range(3):
                print(row, col)

                device.shell("input tap 110 1170")  # Data from picture
                time.sleep(2)
                device.shell("input tap 62 1360")  # Storage
                time.sleep(4)
                take_screenshot(device)

                img = cv2.imread("screen.png")
                result = cv2.matchTemplate(img, folder, cv2.TM_CCOEFF_NORMED)

                if np.unravel_index(result.argmax(), result.shape)[1] < 100:
                    commands = [
                        "input tap 50 130",  # Menu
                        "input tap 50 1030",  # pythontesin
                        "input tap 250 360",  # mydrive
                        "input tap 250 460",  # Pitchbook
                        "input tap 550 460",  # Folder
                    ]
                    for command in commands:
                        print(command)
                        device.shell(command)
                        time.sleep(0.5)

                time.sleep(2)
                for _ in range(page):
                    device.shell(f"input swipe 150 1050 150 400")

                # Select Picture
                device.shell(f"input tap {150 + col*200} {400 + row*200}")
                time.sleep(9)
                device.shell("input tap 608 1480")  # Continue
                time.sleep(12)
                device.shell("input tap 350 1460")  # Open
                time.sleep(4)
                device.shell("input tap 150 1460")  # Open Anyway

                for _ in range(27):
                    device.shell("input keyevent 20")  # Down

                progress.update(task1, advance=1)
