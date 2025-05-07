import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import webbrowser

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
    worksheet = spreadsheet.worksheet("Weekly_stat")
except gspread.exceptions.WorksheetNotFound:
    worksheet = spreadsheet.add_worksheet(title="Weekly_stat", rows="10", cols="2")

# Clear the sheet
worksheet.clear()

# Open the google sheet in my browser
webbrowser.open("https://docs.google.com/spreadsheets/d/1hG5T77pHxbJmRq7azhClm2Ew0YWNR4Z7cQf2gW3w9oY")
