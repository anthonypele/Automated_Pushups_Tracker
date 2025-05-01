import pyautogui as pag
import time
import pyperclip
import datetime
import pygetwindow as gw
import os
import re
import pytz
import tzlocal
import shutil

# ====================================
# --- Getting the messages from WA ---
# ====================================

# Open Whatsapp desctop
pag.hotkey("win", "s") # Open windows search
time.sleep(2)
pyperclip.copy("Whatsapp")
pag.hotkey("ctrl", "v")
time.sleep(0.1)
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

# Select the last message
pag.hotkey('end')
for i in range(20): # Skipping 10 messages at a time
    pag.hotkey('pgup')
for i in range(70): # How many messages approximately to select
    pag.hotkey('space')
    pag.hotkey('up')

# Copy the messages
pag.hotkey('ctrl', 'c')

# Retrieve copied messages
messages = pyperclip.paste()
new_lines = messages.strip().splitlines() # This is so that lines matter and not every letter.

# =======================================================
# --- Convert pusher's time from my timezone to their ---
# =======================================================

# Get your current time zone automatically 
my_timezone = tzlocal.get_localzone()
print("your local time:", datetime.datetime.now(my_timezone))
print("your local time zone", my_timezone)

# Teaching the script how to divide lines into date, time, name and number of pushups
pattern = r"\[(\d{2}\.\d{2}\.\d{4}) (\d{1,2}:\d{2})\] (.*?): (\d+)"

# Map names and timezones
timezones = {
    "Michael Ice&Fire Perm": pytz.timezone('Europe/Madrid'),
    "Anthony": my_timezone,
    "Гриша Соловьев": pytz.timezone('Europe/Moscow'),
    "Павел Антонюк РТ": pytz.timezone('Europe/Moscow'),
    "Андрей Палыч Павлов": pytz.timezone('America/Mexico_City'),
    "Роман Аландаров": pytz.timezone('Europe/Moscow'),
    "Андрей Русанов": pytz.timezone('Europe/Moscow')
}

# Convert to target city timezone
def convert_time(date_str, time_str, pusher_name): 
    # Parse datetime from string (assumed in my timezone)
    naive_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")

    # Attach my timezone to that naive datetime
    my_dt = naive_dt.replace(tzinfo=my_timezone)

    # Get pusher timezone
    pusher_tz = timezones.get(pusher_name, my_timezone) # fallback = your timezone

    # Convert from my time to pusher's time
    pusher_dt = my_dt.astimezone(pusher_tz)

    # Return formatted date and time
    return pusher_dt.strftime("%d.%m.%Y"), pusher_dt.strftime("%H:%M")

# Creating new lines
lines_time_adjusted = []

for line in new_lines:
    match = re.match(pattern, line)
    if match:
        date, timing, name, pushups = match.groups()

        # Time converstion
        new_date, new_time = convert_time(date, timing, name)

        # Form a new line
        line_time_adjusted = f'[{new_date} {new_time}] {name}: {pushups}'
        lines_time_adjusted.append(line_time_adjusted)
    else:
        print(f"Line did not match pattern: {line}")

# ============================
# --- Open/Create the file ---
# ============================

# Get current timestamp - NOT USED
#now = datetime.datetime.now()
#timestamp = now.strftime('%Y-%m-%d_%H-%M-%S') # Format: 2025-04-10_15-42-07

# Create filename with timestamp - Not Used
# Name of the file to append new messages
filename = f"pushups_data.txt"

# Define save folder
save_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data"

# Full path to save the file
file_path = os.path.join(save_folder, filename)

# =======================
# --- Backup the file ---
# =======================

# Extract name and folder
folder = os.path.dirname(file_path)
name_only, ext = os.path.splitext(filename)

# Create backup subfolder if it doesn't exist
backup_folder = os.path.join(folder, "Backup")
os.makedirs(backup_folder, exist_ok=True) # If it exists that it won't run

# Make timestamped backup filename
timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
backup_filename = f'{name_only}_backup_{timestamp_str}{ext}'
backup_path = os.path.join(backup_folder, backup_filename)

# Copy original file to backup location
shutil.copy(file_path, backup_path)
print(f'🔒 Backup saved to: {backup_path}')

# ===========================
# --- Update and the file ---
# ===========================

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

# Paste retrived messages into the txt file
append_unique_lines(file_path, lines_time_adjusted)

# =====================
# --- Sort the file ---
# =====================

# Read and clean lines
with open(file_path, 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file if line.strip()]

# Extract date time
def Extract_datetime(line):
    try:
        timestamp = line.split(']')[0].strip('[')
        return datetime.datetime.strptime(timestamp, "%d.%m.%Y %H:%M")
    except:
        print(f"⚠️ Could not parse line: {line} — Error")
        return datetime.datetime.min

# Sort lines
lines.sort(key=Extract_datetime) #Oldest first
#lines.sort(key=Extract_datetime, reverse=True) #Newest first

# Overwrite with sorted content
with open(file_path, 'w', encoding='utf-8') as file:
    for line in lines:
        file.write(line + '\n')

print('✅ File sorted and overwritten successfully')




# Open the file, that was created (Optional)
os.startfile(file_path)

# Debugging what is happening with the lines
#print(repr(new_lines))
#print(type(new_lines))
