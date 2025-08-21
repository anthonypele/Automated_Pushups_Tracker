import psycopg2
import pandas as pd
from utilities.choose_file import choose_file
from utilities.aliases import aliases
import re
import datetime
import os

with open(choose_file(), 'r', encoding='UTF-8') as file:
    lines = file.readlines()

pattern = r"\[(\d{2}\.\d{2}\.\d{4}) (\d{1,2}:\d{2})\] (.*?): (\d+)"

data_csv = ['date,time,pusher,pushups']

# Parse lines
for line in lines: 
    match = re.match(pattern, line.strip())
    if match:
        date_str, time, name, pushups = match.groups()
        date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
        alias = aliases.get(name, name)
        postgres_date = datetime.datetime.strftime(date, '%Y-%m-%d')
        data_csv.append(
        f'{postgres_date},{time},{alias},{pushups}'
        )

#print(data_csv)

# %% ==================
# Saving the file
# ==================
# Get current timestamp 
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d_%H-%M-%S') # Format: 2025-04-10_15-42-07

# Create filename with timestamp
filename = f"pushups_data_{timestamp}.csv"

# Define save folder
save_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data\csv_data"

# Full path to save the file
file_path = os.path.join(save_folder, filename)

# Save to excel - This is to save only 1 sheet. For multilple use panda
#pivot.to_excel(file_path)

#lines_csv = data_csv.readlines()

# Save csv
with open(file_path, 'a', encoding='UTF-8') as file:
    for line in data_csv:
        clean_line = line.strip()
        file.write(clean_line + '\n')

# os.startfile(file_path)


# load CSV
df = pd.read_csv(file_path)

conn = psycopg2.connect(
    dbname = "pushups_data",
    user = "postgres",
    password = "Pushharder100",
    host = "localhost",
    port = "5432"
)
cursor = conn.cursor()

# Loop through rows and insert with ON CONFLICT
for row in df.itertuples(index=False):
    cursor.execute("""
        INSERT INTO "Last 2 weeks" (date, time, name, pushups)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (row.date, row.time, row.pusher, row.pushups))

conn.commit()
cursor.close()
conn.close()

# conn2 = psycopg2.connect()