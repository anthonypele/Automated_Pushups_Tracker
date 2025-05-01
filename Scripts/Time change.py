import os
import datetime
import shutil
import tkinter as tk
from tkinter import filedialog
from zoneinfo import ZoneInfo
import pytz
import re
import tzlocal 

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
os.makedirs(backup_folder, exist_ok=True) # If it exists that it won't run

# Make timestamped backup filename
timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
backup_filename = f'{name_only}_backup_{timestamp_str}{ext}'
backup_path = os.path.join(backup_folder, backup_filename)

# Copy original file to backup location
shutil.copy(file_path, backup_path)
print(f'🔒 Backup saved to: {backup_path}')

# Extract date time - from previous idea, now it will be included into convert_time function
#def Extract_datetime(line):
#    try:
#        timestamp = line.split(']')[0].strip('[')
#        return datetime.strptime(timestamp, "%d.%m.%Y %H:%M")
#    except:
#        print(f"⚠️ Could not parse line: {line} — Error: {e}")
#        return datetime.min

# Get your current time zone automatically 
my_timezone = tzlocal.get_localzone()
print("your local time:", datetime.datetime.now(my_timezone))
print("your local time zone", my_timezone)

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
def convert_time_wrong(date_str, time_str, pusher_name):
    # Parse datetime from string    
    local_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")

    # Attach pusher timezone
    pusher_tz = timezones.get(pusher_name, my_timezone) # fallback = your timezone

    if isinstance(pusher_tz, pytz.BaseTzInfo):
        localized_dt = pusher_tz.localize(local_dt)
    else:
        localized_dt = local_dt.replace(tzinfo=pusher_tz)

    # Convert to your timezone
    my_dt = localized_dt.astimezone(my_timezone)

    # Return formatted date and time
    return my_dt.strftime("%d.%m.%Y"), my_dt.strftime("%H:%M")

def convert_time(date_str, time_str, pusher_name): # ITs' in the APT 3 small questions chat
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

# --- Main ---

# Read and clean lines
with open(file_path, 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file if line.strip()]

new_lines = []

for line in lines:
    match = re.match(pattern, line)
    if match:
        date, time, name, pushups = match.groups()

        # Time converstion
        new_date, new_time = convert_time(date, time, name)

        # Form a new line
        new_line = f'[{new_date} {new_time}] {name}: {pushups}'
        new_lines.append(new_line)
    else:
        new_lines.append(line) # In case line doesn't match pattern


# Sort lines - next time
#new_lines.sort(key=new_date) #Oldest first
#lines.sort(key=Extract_datetime, reverse=True) #Newest first

# Overwrite with sorted content
with open(file_path, 'w', encoding='utf-8') as file:
    for line in new_lines:
        file.write(line + '\n')

print('✅ File sorted and overwritten successfully')
os.startfile(file_path)