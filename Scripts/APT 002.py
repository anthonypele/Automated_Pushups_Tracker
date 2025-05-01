from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up WebDriver (Ensure you have ChromeDriver installed)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument(r"user-data-dir=C:\Users\Anthony\AppData\Local\Google\Chrome\User Data") #Change this path!
chrome_options.add_argument(r"profile-directory=Default") 

service = Service("C://Users/Anthony/YandexDisk/_Programming/ATP/chromedriver-win64/chromedriver-win64/chromedriver.exe")

driver = webdriver.Chrome(service=service, options=chrome_options) # Open Chrome
driver.get("https://web.whatsapp.com") # Load WhatsApp Web

print("Scan the QR code to log in")
time.sleep(5) #Wait for manual Login

# Decided to try different way to get to whatsapp data