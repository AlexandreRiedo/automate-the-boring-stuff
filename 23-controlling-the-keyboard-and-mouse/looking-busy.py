import pyautogui

dist = 1
interval = 10

while True:
    pyautogui.move(-dist, 0)
    pyautogui.sleep(interval)
    pyautogui.move(dist, 0)
    pyautogui.sleep(interval)
