# Libraries and utilities exports
import datetime
import shutil
import os
import re

from utilities.choose_file import choose_file
from utilities.timezones import timezones
from utilities.timezones import get_my_timezone
from utilities.convert_time import convert_time


# Establish the pattern of the correct data lines
pattern_with_seconds = r"\[(\d{2}\.\d{2}\.\d{4}), (\d{2}:\d{2}):\d{2}\] (.*?): (\d+)"

# Read and copy data from the txt file that I chose
with open(choose_file(), 'r', encoding='utf-8') as file:
    all_lines = file.readlines() #creating a list made of each line from the txt

# Keep only lines that match the pattern + adjust the time
converted_lines = []
skipped_lines = []

for line in all_lines:
    line = line.strip()
    match = re.match(pattern_with_seconds, line)
    if match:
        date, time, name, number = match.groups()
        # Time converstion
        new_date, new_time = convert_time(date, time, name)

        # Form a new line
        formatted_line = f'[{new_date} {new_time}] {name}: {number}'
        converted_lines.append(formatted_line)
    else:
        skipped_lines.append(line)

print(f"✅ Found {len(converted_lines)} valid lines")
print(f"⚠️ Skipped {len(skipped_lines)} lines")

# =========================================
# --- Define the file to append data to ---
# =========================================

# Name of the file to append new messages
filename = f"pushups_data3.txt"

# Define save folder. If I use a timestamp - then add Data\Txt_data
save_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data"

# Full path to save the file
file_path = os.path.join(save_folder, filename)

# ====================================================
# --- Backup pushups txt data in case I mess it up ---
# ====================================================

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

# =============================================
# --- Update the file and check for doubles ---
# =============================================

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
append_unique_lines(file_path, converted_lines)

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
lines.sort(key=Extract_datetime, reverse=True) #Oldest first
#lines.sort(key=Extract_datetime, reverse=True) #Newest first

# Overwrite with sorted content
with open(file_path, 'w', encoding='utf-8') as file:
    for line in lines:
        file.write(line + '\n')

print('✅ File sorted and overwritten successfully')


# Open the file, that was created (Optional)
os.startfile(file_path)