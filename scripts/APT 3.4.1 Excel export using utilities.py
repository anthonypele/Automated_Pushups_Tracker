# %% Load libraries
import datetime
import os
import pandas as pd

# Imports from my utilities
from utilities.excel_and_pivot import excel_and_pivot

# %% ==================
# Saving the file
# ==================
# Get current timestamp 
now = datetime.datetime.now()
timestamp = now.strftime('%Y-%m-%d_%H-%M-%S') # Format: 2025-04-10_15-42-07

# Create filename with timestamp
filename = f"pushups_data_{timestamp}.xlsx"

# Define save folder
save_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data\Xlsx_data"

# Full path to save the file
file_path = os.path.join(save_folder, filename)

# Save to excel - This is to save only 1 sheet. For multilple use panda
#pivot.to_excel(file_path)

# Save multiple sheets to excel
df, filtered_pivot, filtered_pivot2 = excel_and_pivot()
with pd.ExcelWriter(file_path, engine='openpyxl', date_format="DD.MM.YYYY") as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
    filtered_pivot2.to_excel(writer, sheet_name='Count')
    filtered_pivot.to_excel(writer, sheet_name='Last_2_months')

# Style the data
    workbook = writer.book
    sheet = writer.sheets['Last_2_months']
    for row in range(2, sheet.max_row + 1):
        cell = sheet.cell(row=row, column=sheet.max_column)
        cell.number_format = '0%'
    sheet = writer.sheets['Count']
    for row in range(2, sheet.max_row + 1):
        cell = sheet.cell(row=row, column=sheet.max_column)
        cell.number_format = '0%'

print("✅ Data successfully exported to {file path}")

os.startfile(file_path)

