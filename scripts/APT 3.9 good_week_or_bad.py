import psycopg2
import pandas as pd
from tabulate import tabulate
import pyperclip

import tkinter as tk
from tkinter import filedialog
import re
import datetime
from collections import defaultdict
import os
import time

# Imports from my Utilities
from utilities.aliases import aliases
from utilities.choose_file import choose_file

#%% Getting the data of goodness of days from postgres

conn = psycopg2.connect(
    dbname = "pushups_data",
    user = "postgres",
    password = "Pushharder100",
    host = "localhost",
    port = "5432"
)

df = pd.read_sql("""
WITH actual AS (
	SELECT name, date, pushups FROM "Last 2 weeks" WHERE date >= CURRENT_DATE - INTERVAL '1.5 year'
),
clean AS (
	SELECT
		name,
		PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY pushups) AS high,
		PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY pushups) AS low,
		PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pushups) AS mediana
	FROM "actual"
	GROUP BY name
),
normal AS (
	SELECT name, date, pushups
	FROM "actual"
	JOIN clean c USING(name)
	WHERE pushups <= high AND pushups >= low
),
full_data AS (
	SELECT name, ROUND(STDDEV(pushups), 0) AS sd_full
	FROM "actual"
	GROUP BY name
),
normal_sd AS (
	SELECT
		name,
		(ROUND(AVG(pushups), 0) - ROUND(STDDEV(pushups), 0)) AS norm_min,
		(ROUND(AVG(pushups), 0) + ROUND(STDDEV(pushups), 0)) AS norm_max
	FROM "normal"
	GROUP BY name
)
SELECT
	name,
	ROUND(low::numeric, 0) AS low,
	nsd.norm_min AS norm_low,
	nsd.norm_max AS norm_high,
	ROUND(high::numeric, 0) AS high
FROM "normal" n
JOIN full_data f USING(name)
JOIN clean c USING(name)
JOIN normal_sd nsd USING(name)
GROUP BY name, low, norm_low, norm_high, high
ORDER BY low DESC  
""", conn)

tab_beauty = tabulate(df, headers='keys', tablefmt='psql', showindex=False)

limits = df.set_index('name')[['low','norm_low','norm_high','high']].to_dict(orient='index')

# pyperclip.copy(tab_beauty)
# print(tab_beauty)

conn.commit()
# cursor.close()
conn.close()

#%% Open a file dialog to choose a file
with open(r"c:\Users\Anthony\YandexDisk\_Programming\APT\Data\pushups_data2.txt", 'r', encoding="utf-8") as file:
    lines = file.readlines() #creating a list made of each line from the txt imported WA file

# Calculating last week's date range
today = datetime.date.today()
start_of_this_week = today - datetime.timedelta(days=today.weekday())
start_of_last_week = start_of_this_week - datetime.timedelta(days=7)
end_of_last_week = start_of_this_week - datetime.timedelta(days=1)

# A place to store the pushups count
totals_last_week = defaultdict(int)
days_count = defaultdict(int)

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
        display_name = aliases.get(name, name) # Changing names for the correct ones
        if start_of_last_week <= date <= end_of_last_week:
            totals_last_week[display_name] += pushups
            days_count[display_name] += 1

# Prepare all names
#all_names = set(totals_last_week)

# creating print_and_save function, so that I can collect all the printed text in the terminal and save it for pasting
output_text = ""
def print_and_save(text):
    global output_text
    print(text)
    output_text += text + "\n"

#display_name = aliases.get(name, name) # Get the preferable name or use the basic one if it's not in the dictionary aliases

print_and_save(f"\n*Какая была неделя для каждого с {start_of_last_week} по {end_of_last_week}:*\n")
for name in sorted(totals_last_week, key=lambda n: totals_last_week.get(n, 0), reverse=True):
    display_name = aliases.get(name, name)
    total = totals_last_week.get(name, 0)
    # avg = round(total / days_count.get(name, 0))
    avg = round(total / 7)

    #last_week = totals_last_week.get(name, 0) # making sure if the name doesn't exist this week, then it has 0, using extra variable for readability

    if limits[display_name]['low'] == limits[display_name]['high'] and avg == limits[display_name]['low']:
        print_and_save(f"{display_name}: {avg} - нормальная неделя 👌")
    elif avg > limits[display_name]['high'] :
    	print_and_save(f"{display_name}: {avg} - огненная неделя 🌋")
    elif limits[display_name]['high'] >= avg >= limits[display_name]['norm_high'] :
    	print_and_save(f"{display_name}: {avg} - мощная неделя 🦍")
    elif limits[display_name]['norm_high'] > avg >= limits[display_name]['norm_low'] :
        print_and_save(f"{display_name}: {avg} - нормальная неделя 👌")
    elif limits[display_name]['norm_low'] > avg >= limits[display_name]['low'] :
        print_and_save(f"{display_name}: {avg} - усталая неделя 🐌")
    else:
        print_and_save(f"{display_name}: {avg} - убитая неделя 🫠")

# Copy all the printed text into the clipboard
#pyperclip.copy(output_text)

final_text = output_text + '\n' + tab_beauty
pyperclip.copy(final_text)
print(tab_beauty)

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
with open(message_file_path, 'a', encoding="utf-8") as file:
    file.write(output_text)