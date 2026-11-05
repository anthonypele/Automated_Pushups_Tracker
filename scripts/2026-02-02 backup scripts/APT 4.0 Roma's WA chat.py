# Import libraries
import pyautogui as pag
import pyperclip
import pygetwindow as gw
import time

from utilities.aliases import aliases
from utilities.timezones import timezones

# Using keyboard
pag.hotkey('win', 's')
pyperclip.copy('Whatsapp')
pag.hotkey('ctrl','v')
pag.press('enter')
time.sleep(1)
pag.press('esc')


# Making the WA window maximized
whatsapp = gw.getWindowsWithTitle('Whatsapp')[0]
whatsapp.activate()
if not whatsapp.isMaximized:
    whatsapp.activate()
    whatsapp.maximize()

# Find the chat

pag.hotkey('ctrl', 'f')
time.sleep(0.5)
pyperclip.copy('Тренировки')
pag.hotkey('ctrl', 'a') # to ensure previous search is not added
pag.hotkey('ctrl', 'v')
time.sleep(0.5)
pag.press('enter')
pag.press('down')
time.sleep(0.5)
pag.press('enter')
time.sleep(1)

# click the mouse inside the chat to start selecting messages
input_w, input_h = pag.size()
input_x = input_w * 0.29
input_y = input_h * 0.25
pag.click(input_x, input_y, button='right')
time.sleep(1)

# get to selection mode
pag.press('tab')
pag.press('enter')

# select the messages and copy 'em
pag.press('end')
for i in range (6):
    pag.press('space')
    pag.press('up')
pag.hotkey('ctrl', 's') # save selected messages 
time.sleep(1)
pag.press('esc')