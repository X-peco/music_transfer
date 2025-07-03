import pyautogui
import time
import keyboard

def find_and_click_in():
    try:
        # 设置匹配阈值（0~1，越高越严格，建议 0.7~0.9）
        confidence = 0.8
        location = pyautogui.locateOnScreen('in.png', confidence=confidence)
        if location:
            print("✅成功加入")
            heart_x, heart_y = pyautogui.center(location)
            pyautogui.moveTo(heart_x, heart_y, duration=0.3)
            pyautogui.click()
            return location
        else:
            print("❌未加入")
            return False
    except Exception as e:
        print(f"❌识别异常: {e}")
        return False
def find_and_click_add():
    try:
        # 设置匹配阈值（0~1，越高越严格，建议 0.7~0.9）
        confidence = 0.8
        location = pyautogui.locateOnScreen('add.png', confidence=confidence)
        if location:
            print("✅成功添加")
            heart_x, heart_y = pyautogui.center(location)
            pyautogui.moveTo(heart_x, heart_y, duration=0.3)
            pyautogui.click()
            return location
        else:
            print("❌未找到添加")
            return False
    except Exception as e:
        print(f"❌识别异常: {e}")
        return False

def find_and_click_search():
    try:
        # 设置匹配阈值（0~1，越高越严格，建议 0.7~0.9）
        confidence = 0.8
        location = pyautogui.locateOnScreen('search.png', confidence=confidence)
        if location:
            print("✅成功进入听歌识曲")
            heart_x, heart_y = pyautogui.center(location)
            pyautogui.moveTo(heart_x, heart_y, duration=0.3)
            pyautogui.click()
            return location
        else:
            print("❌未找到听歌识曲")
            return False
    except Exception as e:
        print(f"❌识别异常: {e}")
        return False

def find_and_click_cloudmusic():
    try:
        # 设置匹配阈值（0~1，越高越严格，建议 0.7~0.9）
        confidence = 0.8
        location = pyautogui.locateOnScreen('cloudmusic.png', confidence=confidence)
        if location:
            print("✅成功进入网易")
            heart_x, heart_y = pyautogui.center(location)
            pyautogui.moveTo(heart_x, heart_y, duration=0.3)
            pyautogui.click()
            return location
        else:
            print("❌未找到网易")
            return False
    except Exception as e:
        print(f"❌识别异常: {e}")
        return False

def find_and_click_heart():
        confidence = 0.8
        location = pyautogui.locateOnScreen('heart_template.png',confidence=confidence)
        if location:
            temp=find_and_click_cloudmusic()
            if temp:
                temp=find_and_click_search()
                if temp:
                    temp=find_and_click_add()
                    if temp:
                        find_and_click_in()
pause=False
while True:
    if keyboard.is_pressed('q'):
        print('🚫')
        break
    elif keyboard.is_pressed('ctrl+p'):
        pause=True
    elif keyboard.is_pressed('ctrl+r'):
        pause=False
    if not pause:
        find_and_click_heart()
        time.sleep(3)