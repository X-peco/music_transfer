import os
import pyautogui
import time

time.sleep(4)
x,y=pyautogui.position()
heart_full = 'search.png'
pyautogui.screenshot(heart_full, region=(x - 20, y - 20, 40, 40))
full_path = os.path.join(os.getcwd(), heart_full)
print(f"截图文件的完整路径是: {full_path}")

def find():
    confidence = 0.8
    location = pyautogui.locateOnScreen('search.png', confidence=confidence)
    try:
        if location:
            print("⭕\n")
            heart_x, heart_y = pyautogui.center(location)
            pyautogui.moveTo(heart_x, heart_y, duration=0.3)
            pyautogui.click()
        else:
            print("❌")
    except Exception as e:
        print(f"{e}")


find()