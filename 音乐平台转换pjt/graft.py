import pyautogui
import time
import os
time.sleep(4)
x,y=pyautogui.position()
heart_full = 'search.png'
pyautogui.screenshot(heart_full, region=(x - 20, y - 20, 40, 40))
full_path = os.path.join(os.getcwd(), heart_full)
print(f"截图文件的完整路径是: {full_path}")