import pyautogui as pag
import pyperclip
import time
import datetime
import os

# Define the folder to save files
save_folder = "C:\\Users\\Anthony\\YandexDisk\\_Programming\\ATP\\Data"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Generate the current date for filename
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
filename = f"pushups_{current_date}.txt"
file_path = os.path.join(save_folder, filename)

# Open Notepad
pag.hotkey("win", "r")
time.sleep(1)
pyperclip.copy("notepad")
pag.hotkey("ctrl", "v")
pag.press("enter")
time.sleep(2)

# Write text into Notepad
message = "Today I did 39 pushups!"
pyperclip.copy(message)
pag.hotkey("ctrl", "v")

# Open Save As dialog
pag.hotkey("ctrl", "s")
time.sleep(1)

# Paste the file path, save and overwrite the previous one, if needed
pyperclip.copy(file_path)
pag.hotkey("ctrl", "v")
pag.press("Enter")
time.sleep(2)
pag.hotkey("ctrl", "w")

print(f"File saved at: {file_path}")