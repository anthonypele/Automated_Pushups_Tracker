import pyautogui as pag
import pyperclip
import time
import datetime
import os

# New variables
# doesn't work, starts to paste it in the VS Code OoO paste = pag.hotkey("ctrl", "v")

# Open Whatsapp desctop
pag.hotkey("win", "s") # Open windows search
time.sleep(1)
pyperclip.copy("Whatsapp")
pag.hotkey("ctrl", "v")
pag.press("enter")
time.sleep(3)

# Search for the group
pag.hotkey("ctrl", "f")
time.sleep(1)
group_name = "Отжимания утром"
pyperclip.copy(group_name)
pag.hotkey("ctrl", "v")
pag.hotkey("tab")
pag.press("enter")
time.sleep(2)

# Click inside the chat to start selecting messages
chat_x, chat_y = 1000, 500
pag.click(chat_x, chat_y, button="right")
time.sleep(1)

# Select selection mode
chat_x += 15 # Move 15 pixels to the right
chat_y += 15 # Move 15 pixels down
pag.click(chat_x, chat_y, button="left")
time.sleep(1)

# Select and copy the messages
pag.hotkey("tab")
pag.hotkey("shift", "tab")
pag.hotkey("end") # to ensure that it goes to the last message
pag.hotkey("space")
pag.hotkey("up")
pag.hotkey("space")
pag.hotkey("ctrl", "c")
time.sleep(2)

# Retrieve copied messages
messages = pyperclip.paste()

# Define save folder
save_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data"

# Get last week's number
today = datetime.date.today()
start_of_this_week = today - datetime.timedelta(days=today.weekday())
start_of_last_week = start_of_this_week - datetime.timedelta(days=7)
last_week_number = start_of_last_week.isocalendar()[1] 

# Create the filename
filename = f"pushups_week_{last_week_number}.txt"
file_path = os.path.join(save_folder, filename)

# Save messages to the file 
with open(file_path, "w", encoding="utf-8") as file:
    file.write(messages)

print(f"Messages saved successfully as {filename}!")

os.startfile(file_path)