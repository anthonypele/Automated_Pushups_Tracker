import pyautogui as pag
import time
import pyperclip
import datetime
import pygetwindow as gw
import os

# This program works when whatsapp app window is opened and is full screen and it was used previously so that alt + tab works

# Open Whatsapp desctop
pag.hotkey("win", "s") # Open windows search
time.sleep(1)
pyperclip.copy("Whatsapp")
pag.hotkey("ctrl", "v")
pag.press("enter")
time.sleep(3)

# Naming WA app
windows = gw.getWindowsWithTitle("Whatsapp")
if windows:
    whatsapp = windows[0]

# Make sure WA app is full screen
if not whatsapp.isMaximized:
    whatsapp.activate()
    whatsapp.maximize()

# Search for the group
pag.hotkey("ctrl", "f")
time.sleep(1)
group_name = "Отжимания утром"
pyperclip.copy(group_name)
pag.hotkey("ctrl", "a") # to ensure previous search is not added
pag.hotkey("ctrl", "v")
pag.hotkey("tab")
pag.press("enter")
time.sleep(2)

# Click inside the chat to start selecting messages
chat_x, chat_y = 750, 550
pag.click(chat_x, chat_y, button="right")
time.sleep(1)

# Select selection mode
pag.hotkey('tab')
pag.hotkey('enter')

# Select the last message
pag.hotkey('end')
for i in range(20):
    pag.hotkey('space')
    pag.hotkey('up')

# Copy the messages
pag.hotkey('ctrl', 'c')

# Retrieve copied messages
messages = pyperclip.paste()

# Get current timestamp
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d_%H-%M-%S') # Format: 2025-04-10_15-42-07

# Create filename with timestamp
filename = f"pushups_test_{timestamp}.txt"

# Define save folder
save_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data"

# Full path to save the file
file_path = os.path.join(save_folder, filename)

# Paste retrived messages into the txt file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(messages)

# Open the file, that was created (Optional)
os.startfile(file_path)