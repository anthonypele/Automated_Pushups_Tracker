import tkinter as tk
from tkinter import filedialog
import re
import datetime
from collections import defaultdict
import os
import pyperclip

# Imports from my Utilities
from utilities.aliases import aliases
from utilities.choose_file import choose_file

# Open a file dialog to choose a file
with open(choose_file(), 'r', encoding="utf-8") as file:
    lines = file.readlines() #creating a list made of each line from the txt imported WA file

# Calculating last week's date range
today = datetime.date.today()
start_of_this_week = today - datetime.timedelta(days=today.weekday())
start_of_last_week = start_of_this_week - datetime.timedelta(days=7)
end_of_last_week = start_of_this_week - datetime.timedelta(days=1)
start_of_week_before_last = start_of_this_week - datetime.timedelta(days=14)
end_of_week_before_last = start_of_this_week - datetime.timedelta(days=8)

# A place to store the pushups count
totals_last_week = defaultdict(int)
totals_week_before_last = defaultdict(int)
days_count_last_week = defaultdict(int)
days_count_week_before_last = defaultdict(int)

# Find useful info in each line using a regex pattern
pattern = re.compile(r"\[(\d{2}\.\d{2}\.\d{4}) \d{1,2}:\d{2}] (.*?): (\d+)")

# Loop through each line and extract data
for line in lines:
    match = pattern.search(line)
    if match:
        date_str, name, pushups = match.groups()

        # Convert the date and check if it's from last week
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

        #Make pushups integer
        pushups = int(pushups)

        if start_of_last_week <= date <= end_of_last_week:
            totals_last_week[name] += pushups
            days_count_last_week[name] += 1
        elif start_of_week_before_last <= date <= end_of_week_before_last:
            totals_week_before_last[name] += pushups
            days_count_week_before_last[name] += 1

# Prepare all names across both weeks
all_names = set(totals_last_week) | set(totals_week_before_last)

# creating print_and_save function, so that I can collect all the printed text in the terminal and save it for pasting
output_text = ""
def print_and_save(text):
    global output_text
    print(text)
    output_text += text + "\n"

# Calculating the difference 
diff_pushups = {}
for name in all_names:
    last = totals_last_week[name]
    previous = totals_week_before_last.get(name, 0)
    diff_pushups[name] = last - previous

diff_days = {}
for name in all_names:
    last = days_count_last_week.get(name, 0)
    previous = days_count_week_before_last.get(name, 0)
    diff_days[name] = last - previous

print_and_save(f"\nВсего отжиманий на прошлой неделе с {start_of_last_week} по {end_of_last_week}:\n")
for name in sorted(all_names, key=lambda n: totals_last_week.get(n, 0), reverse=True):

    display_name = aliases.get(name, name) # Get the preferable name or use the basic one if it's not in the dictionary aliases

    last_week = totals_last_week.get(name, 0) # making sure if the name doesn't exist this week, then it has 0, using extra variable for readability

    if diff_pushups.get(name, 0) > 0:
        print_and_save(f"{display_name}: {last_week}, это больше на {diff_pushups[name]}, чем на неделе до 💪")
    elif diff_pushups.get(name, 0) < 0:
        print_and_save(f"{display_name}: {totals_last_week.get(name, 0)}, это меньше на {abs(diff_pushups[name])}, чем на неделе до 😴")
    else:
        print_and_save(f"{display_name}: {totals_last_week.get(name, 0)}, ровно 😎")

print_and_save(f"\nДней отжиманий за неделю:\n")
for name in sorted(all_names, key=lambda x: days_count_last_week.get(x, 0), reverse=True):
    display_name = aliases.get(name, name)
    if days_count_last_week.get(name, 0) == days_count_week_before_last.get(name, 0):
        print_and_save(f"{display_name}: {days_count_last_week.get(name, 0)} дн., неделю назад - {days_count_week_before_last.get(name, 0)} дн. Стабильность - признак мастерства")
    else:
        print_and_save(f"{display_name}: {days_count_last_week.get(name, 0)} дн., неделю назад - {days_count_week_before_last.get(name, 0)} дн.")

# Copy all the printed text into the clipboard
pyperclip.copy(output_text)

# Start the txt file to check pasting
#os.startfile(choose_file())

# Create Messages folder, if it doesn't exist
folder = r'C:\Users\Anthony\YandexDisk\_Programming\APT\Data'
message_folder = os.path.join(folder, "Messages")
os.makedirs(message_folder, exist_ok=True) #If it exists than it won't run

# Save the data in the txt file
message_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data\Messages"
message_file = f'{start_of_last_week} - {end_of_last_week} Message.txt'
message_file_path = os.path.join(message_folder, message_file)
with open(message_file_path, 'w', encoding="utf-8") as file:
    file.write(output_text)

