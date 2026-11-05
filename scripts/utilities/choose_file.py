import tkinter as tk
from tkinter import filedialog

def choose_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title='Select the WA data file',
        filetypes=[
            #('Text files', '*.txt'),
            #('JSON files', '*.json'),
            ('Text and JSON', '*.txt *.json')
        ],
        initialdir=r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data"
    )

    return file_path
