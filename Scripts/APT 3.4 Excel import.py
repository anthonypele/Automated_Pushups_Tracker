import tkinter as tk
from tkinter import filedialog
import re
import datetime
import os
import pandas as pd
import openpyxl

# Open a file dialog to choose a file
def choose_file():
    # Create a hidden root window (we don't need it to show up)
    root = tk.Tk()
    root.withdraw() # Hides the Tkinter root window

    # Open the file dialog and return the selected file path
    file_path = filedialog.askopenfilename(title='Select the WA data file', filetypes=[('Textfiles', '*.txt')], initialdir=r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data")

    # Return the selected file path
    return file_path

# Read my txt file
with open(choose_file(), 'r', encoding="utf-8") as file:
    lines = file.readlines() #creating a list made of each line from the txt imported WA file

pattern = r"\[(\d{2}\.\d{2}\.\d{4}) (\d{1,2}:\d{2})\] (.*?): (\d+)"

aliases = {
    "Michael Ice&Fire Perm": "Миша",
    "Anthony": "Антон",
    "Гриша Соловьев": "Гриша",
    "Павел Антонюк РТ": "Паша",
    "Андрей Палыч Павлов": "Палыч",
    "Роман Аландаров": "Рома",
    "Андрей Русанов": "Андрей"
}

# New variables
new_lines = []
data = []

# Changing names
def replace_name(match):
    date, time, name, pushups = match.groups()
    new_name = aliases.get(name, name)
    return f'[{date} {time}] {new_name}: {pushups}'

# Changing my lines
new_lines = [re.sub(pattern, replace_name, line) for line in lines]

# Parse lines
for line in new_lines:
    match = re.match(pattern, line.strip())
    if match:
        date, time, name, pushups = match.groups()
        data.append({
            'date': date,
            'time': time,
            'name': name,
            'pushups': int(pushups)
        })

# Create a DataFrame 
df = pd.DataFrame(data)

# Get current timestamp 
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d_%H-%M-%S') # Format: 2025-04-10_15-42-07

# Create filename with timestamp
filename = f"pushups_data_{timestamp}.xlsx"

# Define save folder
save_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data"

# Full path to save the file
file_path = os.path.join(save_folder, filename)

# Save to excel
df.to_excel(file_path, index=False)

print("✅ Data successfully exported to pushups_data.xlsx")

os.startfile(file_path) 