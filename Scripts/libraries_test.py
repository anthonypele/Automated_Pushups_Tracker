import pyautogui
import pyperclip 

print("PyAutoGUI screen size:", pyautogui.size())
pyperclip.copy("Hello!")
print("Pyperclip test:", pyperclip.paste())
