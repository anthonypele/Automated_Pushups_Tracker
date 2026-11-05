import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import webbrowser
from utilities.excel_and_pivot import excel_and_pivot

help(excel_and_pivot)

# Define scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials
json_path = r"C:\Users\Anthony\YandexDisk\_Programming\automated-pushups-tracker-ddef505feb96.json"
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)

# Authorize client
client = gspread.authorize(creds)

# Open your spreadsheet
#from APT_3_2_analyze_the_data_with_percent import choose_file - No, I am wrong, I don't open the file on pc, it's in the google docs
spreadsheet = client.open("Morning Pushups")

# Select the sheet/tab inside
try:
    raw_worksheet = spreadsheet.worksheet("Raw_data")
except gspread.exceptions.WorksheetNotFound:
    raw_worksheet = spreadsheet.add_worksheet(title="Raw_data", rows="10", cols="2")
try:
    pivot_worksheet = spreadsheet.worksheet("Pushups")
except gspread.exceptions.WorksheetNotFound:
    pivot_worksheet = spreadsheet.add_worksheet(title="Pushups", rows="10", cols="2")
try:
    pivot_worksheet2 = spreadsheet.worksheet("Involvement")
except gspread.exceptions.WorksheetNotFound:
    pivot_worksheet2 = spreadsheet.add_worksheet(title="Involvement", rows="10", cols="2")

# Clear the sheet
raw_worksheet.clear()
pivot_worksheet.clear()
pivot_worksheet2.clear()

# Insert the data into google sheet
df, filtered_pivot, filtered_pivot2 = excel_and_pivot()
set_with_dataframe(raw_worksheet, df)
set_with_dataframe(pivot_worksheet, filtered_pivot, include_index=True)
pivot_worksheet.format("D2:D", {"numberFormat": {"type": "PERCENT", "pattern": "0%"}})
set_with_dataframe(pivot_worksheet2, filtered_pivot2, include_index=True)
pivot_worksheet2.format("D2:D", {"numberFormat": {"type": "PERCENT", "pattern": "0%"}})

# Open the google sheet in my browser
webbrowser.open("https://docs.google.com/spreadsheets/d/1hG5T77pHxbJmRq7azhClm2Ew0YWNR4Z7cQf2gW3w9oY")
