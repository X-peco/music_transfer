import pyautogui
import time
import keyboard

confidence = 0.8
lib=['heart_template.png','cloudmusic.png','search.png','add.png','in.png']

def recognise(pictures,match=0.8):
    key=pyautogui.locateOnScreen(pictures[0],confidence=match)
    if key:
        for sequent in range(1, len(pictures)):
            try:
                location = pyautogui.locateOnScreen(pictures[sequent], confidence=match)
                if location:
                    print(f"⭕{pictures[sequent]}")
                    heart_x, heart_y = pyautogui.center(location)
                    pyautogui.moveTo(heart_x, heart_y, duration=0.3)
                    pyautogui.click()
                else:
                    print(f"❌{pictures[sequent]}")
            except Exception as e:
                print(f"‼️{e}‼️")

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
        recognise()
        time.sleep(3)