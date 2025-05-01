import os
from datetime import datetime
import shutil
import tkinter as tk
from tkinter import filedialog

# Open a file dialog to choose a file
def choose_file():
    # Create a hidden root window (we don't need it to show up)
    root = tk.Tk()
    root.withdraw() # Hides the Tkinter root window

    # Open the file dialog and return the selected file path
    file_path = filedialog.askopenfilename(title='Select the WA data file', filetypes=[('Textfiles', '*.txt')], initialdir=r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data")

    # Return the selected file path
    return file_path

# Choose file
file_path = choose_file()

# Extract name and folder
folder = os.path.dirname(file_path)
filename = os.path.basename(file_path)
name_only, ext = os.path.splitext(filename)

# Create backup subfolder if it doesn't exist
backup_folder = os.path.join(folder, "Backup")
os.makedirs(backup_folder, exist_ok=True) # If it exists than it won't run

# Make timestamped backup filename
timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
backup_filename = f'{name_only}_backup_{timestamp_str}{ext}'
backup_path = os.path.join(backup_folder, backup_filename)

# Copy original file to backup location
shutil.copy(file_path, backup_path)
print(f'🔒 Backup saved to: {backup_path}')

# Read and clean lines
with open(file_path, 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file if line.strip()]

# Extract date time
def Extract_datetime(line):
    try:
        timestamp = line.split(']')[0].strip('[')
        return datetime.strptime(timestamp, "%d.%m.%Y %H:%M")
    except:
        print(f"⚠️ Could not parse line: {line} — Error: {e}")
        return datetime.min

# Sort lines
lines.sort(key=Extract_datetime) #Oldest first
#lines.sort(key=Extract_datetime, reverse=True) #Newest first

# Overwrite with sorted content
with open(file_path, 'w', encoding='utf-8') as file:
    for line in lines:
        file.write(line + '\n')

print('✅ File sorted and overwritten successfully')