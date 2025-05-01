import pyautogui as pag
import time

print('Move your mouse to the right location...')
time.sleep(4)
mouse_x, mouse_y = pag.position()
screen_w, screen_h = pag.size()

width_percent = mouse_x / screen_w
height_percent = mouse_y / screen_h

print(screen_w, screen_h)
print(mouse_x, mouse_y)
print(width_percent, height_percent)