# Open the file of my choosing
import tkinter as tk
from tkinter import filedialog
import re
import datetime
from collections import defaultdict

# Open a file dialog to choose a file
def choose_file():
    # Create a hidden root window (we don't need it to show up)
    root = tk.Tk()
    root.withdraw() # Hides the Tkinter root window

    # Open the file dialog and return the selected file path
    file_path = filedialog.askopenfilename(title='Select the WA data file', filetypes=[('Textfiles', '*.txt')], initialdir=r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data")

    # Return the selected file path
    return file_path

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

print(f"\nPushups totals from {start_of_last_week} to {end_of_last_week}:\n")
for name, totals_last_week in sorted(totals_last_week.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: {totals_last_week}")

print(f"\nPushups totals from {start_of_week_before_last} to {end_of_week_before_last}:\n")
for name, totals_week_before_last in sorted(totals_week_before_last.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: {totals_week_before_last}")

print(f"\nDays of pushups {start_of_last_week} to {end_of_last_week}:\n")
for name, count in sorted(days_count_last_week.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: {count} days")