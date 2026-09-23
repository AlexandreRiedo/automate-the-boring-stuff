import pyautogui
import pyperclip

w = pyautogui.getWindowsWithTitle("Notepad")[0]  # pyright: ignore[reportAttributeAccessIssue]
w.activate()
pyautogui.click(w.left + 100, w.centery)
pyautogui.hotkey("ctrl", "a")
pyautogui.hotkey("ctrl", "c")

print(pyperclip.paste())
