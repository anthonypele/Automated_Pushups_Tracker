import pyautogui as pag
import time
import pyperclip
import datetime
import pygetwindow as gw
import os
import re

# Function, that adds only new lines 
def append_unique_lines(file_path, new_lines):

    if isinstance(new_lines, str):                  #If the line was a string to make a list out of it
        new_lines = new_lines.strip().splitlines()

    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            existing_lines = set(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        existing_lines = set()
    
    with open(file_path, 'a', encoding="utf-8") as file:
        for line in new_lines:
            clean_line = line.strip()
            if clean_line and clean_line not in existing_lines:
                file.write(clean_line + "\n")

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
time.sleep(1)
pag.hotkey("down")
time.sleep(1)
pag.press("enter")
time.sleep(2)

# Click the mouse inside the chat to start selecting messages
screen_w, screen_h = pag.size() # Move the mouse
input_x = screen_w * 0.29
input_y = screen_h * 0.25
pag.click(input_x, input_y, button="right")
time.sleep(1)

# Select selection mode
pag.hotkey('tab')
pag.hotkey('enter')
time.sleep(0.5)

pag.hotkey('end') # Select the last message
time.sleep(0.5)

# Regex to find real messages
pattern = re.compile(r"\[(\d{2}\.\d{2}\.\d{4}) \d{1,2}:\d{2}] (.*?): (\d+)")

# function to get exact amount of messages and miss some to go down the list
def copy_real_messages(target_count, skipped_pages):
     real_messages_count = 0
 
    total_selected = 0
    # Skip the amount of messages
    for i in range(skipped_pages): # Skipping approx 10 messages at a time
        pag.hotkey('pgup')
    while real_messages_count < target_count:
        # keep selecting more until we have enough
        pag.hotkey('space')
        pag.hotkey('up')
        time.sleep(0.1)
        total_selected += 1

        # Copy the messages
        pag.hotkey('ctrl', 'c')
        time.sleep(0.5)

        messages = pyperclip.paste()
        matches = pattern.findall(messages)
        real_messages_count = len(matches)

        print(f"Selected {total_selected} messages, found {real_messages_count} real ones.")

        if real_messages_count >= target_count:
            break
    
    print(f"Successfully copied {real_messages_count} real messages!")
    return messages

# Retrieve copied messages
target = 3
skipped_pages = 0
messages = copy_real_messages(target, skipped_pages)
new_lines = messages.strip().splitlines() # This is so that lines matter and not every letter.

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
append_unique_lines(file_path, new_lines)

# Open the file, that was created (Optional)
os.startfile(file_path)
