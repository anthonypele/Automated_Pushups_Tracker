import tkinter as tk
from tkinter import filedialog

def choose_file():
    # Create a hidden root window (we don't need it to show up)
    root = tk.Tk()
    root.withdraw() # Hides the Tkinter root window

    # Open the file dialog and return the selected file path
    file_path = filedialog.askopenfilename(title='Select the WA data file', filetypes=[('Textfiles', '*.txt')], initialdir=r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data")

    # Return the selected file path
    return file_path