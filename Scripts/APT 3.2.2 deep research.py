import tkinter as tk
from tkinter import filedialog
import re
import datetime
from collections import defaultdict
import os
import pyperclip

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

users_per_day = defaultdict(set)

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

        if start_of_week_before_last <= date <= end_of_last_week:
            users_per_day[date].add(name)


# Prepare all names across both weeks
all_names = set(totals_last_week) | set(totals_week_before_last)

# How do I want names to be displayed in the final report
aliases = {
    "Michael Ice&Fire Perm": "Миша",
    "Anthony": "Антон",
    "Гриша Соловьев": "Гриша",
    "Павел Антонюк РТ": "Паша",
    "Андрей Палыч Павлов": "Палыч",
    "Роман Аландаров": "Рома"
}

# creating print_and_save function, so that I can collect all the printed text in the terminal and save it for pasting
output_text = ""
def print_and_save(text):
    global output_text
    print(text)
    output_text += text + "\n"

# Count unique users per day and group by week
def count_users_by_week(start_date, end_date):
    week_data = {date: users for date, users in users_per_day.items() if start_date <= date <= end_date}
    return week_data


print_and_save(f"\nКоличество писавших на прошлой неделе {start_of_last_week} - {end_of_last_week}:\n")
last_week_date = count_users_by_week(start_of_last_week, end_of_last_week)
last_week_total_count = 0 # Create total counter
for date in sorted(last_week_date):
    count = len(last_week_date[date])
    last_week_total_count += count # Add this day's count to total
    print_and_save(f"{date}: {count} человек")
print_and_save(f"Всего на прошлой неделе: {last_week_total_count}")

print_and_save(f"Количество писавших на позапрошлой неделе {start_of_week_before_last} - {end_of_week_before_last}:\n")
week_before_last_date = count_users_by_week(start_of_week_before_last, end_of_week_before_last)
week_before_last_total_count = 0 # Create another total counter
for date in sorted(week_before_last_date):
    count = len(week_before_last_date[date])
    week_before_last_total_count += count
    print_and_save(f"{date}: {count} человек")
print_and_save(f"Всего на позапрошлой неделе: {week_before_last_total_count}")
difference = (last_week_total_count/week_before_last_total_count-1)*100
print(f"\nИтог - с вводом статистики все стали отписываться на {difference}% больше")


# Copy all the printed text into the clipboard
pyperclip.copy(output_text)


