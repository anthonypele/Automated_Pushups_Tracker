import tkinter as tk
from tkinter import filedialog
import re
import datetime
from collections import defaultdict
import time
import pyperclip
import webbrowser
import pyautogui as pag
import os
import pygetwindow as gw

# Imports from my Utilities
from utilities.aliases import aliases

# Open a file dialog to choose a file
from utilities.choose_file import choose_file

with open(choose_file(), 'r', encoding="utf-8") as file:
    lines = file.readlines() #creating a list made of each line from the txt imported WA file

# Calculating last week's date range
today = datetime.date.today()
start_of_this_week = today - datetime.timedelta(days=today.weekday())
start_of_last_week = start_of_this_week - datetime.timedelta(days=7)
end_of_last_week = start_of_this_week - datetime.timedelta(days=1)
start_of_week_before_last = start_of_this_week - datetime.timedelta(days=14)
end_of_week_before_last = start_of_this_week - datetime.timedelta(days=8)

# Find useful info in each line using a regex pattern
pattern = re.compile(r"\[(\d{2}\.\d{2}\.\d{4}) \d{1,2}:\d{2}] ([^:]+): (\d+)")

# Prepare all names across both weeks
#all_names = set(totals_last_week) | set(totals_week_before_last)

# =======================================
# Getting ready the list to feed ChatGPT
# =======================================

# A place to store the pushups count
lines_last_week = []
lines_week_before_last = []

# Getting the correct data
for line in lines:
    match = pattern.search(line)
    if match:
        date_str, name, pushups = match.groups()

        # Convert the date and check if it's from last week
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

        if start_of_last_week <= date <= end_of_last_week:
            lines_last_week.append(line.strip())
        elif start_of_week_before_last <= date <= end_of_week_before_last:
            lines_week_before_last.append(line.strip())
 
 # Changing names
def replace_name(match):
    date, name, pushups = match.groups()
    new_name = aliases.get(name, name)
    return f'[{date}] {new_name}: {pushups}'

# Changing my lines
new_lines_last_week = [re.sub(pattern, replace_name, line) for line in lines_last_week]
new_lines_week_before_last = [re.sub(pattern, replace_name, line) for line in lines_week_before_last]


pyperclip.copy(f'Please analyze following data. Make 10 awards like before in Russian based on this data:\n Last week: {new_lines_last_week}\n Week before the last: {new_lines_week_before_last} \nMake it funny, but still encouraging, it is important that every user has at least 1 award and 2 awards for the whole team of all users')
#print(f'Please analyze following data. Make 10 awards like before in Russian based on this data:\n Last week: {new_lines_last_week}\n Week before the last: {new_lines_week_before_last}')

# Open ChatGPT window
webbrowser.open_new("https://chatgpt.com/c/68068943-d4ec-800e-8920-ad328f1720a0")
time.sleep(3)

# === maximize the window ===
# get all open windows
#all_windows = gw.getAllWindows()

# Sort the by their internal window ID (_hWnd) to guess the newest one
#latest_window = sorted(all_windows, key=lambda w: w._hWnd, reverse=True)[0]

# Activate and maximize that window
#latest_window.activate()
#if not latest_window.isMaximized:
#   latest_window.maximize()

# === Working with ChatGPT ===
# Move the mouse to the right place
screen_w, screen_h = pag.size() # Move the mouse
input_x = screen_w * 0.55
input_y = screen_h * 0.83
pag.click(input_x, input_y)
time.sleep(1)
pag.hotkey('ctrl', 'v')
#pag.press("enter") #Unhashtag to actually get a new message
#time.sleep(10)

# Copy ChatGPT message
input_x2 = screen_w * 0.36
input_y2 = screen_h * 0.52
pag.click(input_x2, input_y2)
pag.hotkey('tab')
#for i in range(6): # Didn't work
#    pag.hotkey('shift', 'tab')
pag.press('enter')
ChatGPT_awards = pyperclip.paste()

# Create Messages folder, if it doesn't exist
folder = r'C:\Users\Anthony\YandexDisk\_Programming\APT\Data'
message_folder = os.path.join(folder, "Messages")
os.makedirs(message_folder, exist_ok=True) #If it exists than it won't run

# Save the data in the txt file
message_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data\Messages"
message_file = f'{start_of_last_week} - {end_of_last_week} Awards.txt'
message_file_path = os.path.join(message_folder, message_file)
with open(message_file_path, 'w', encoding="utf-8") as file:
    file.write(ChatGPT_awards)

os.startfile(message_file_path)