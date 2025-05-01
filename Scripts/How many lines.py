import os

# Create filename with timestamp
filename = f"pushups_data.txt"

# Define save folder
save_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data"

# Full path to save the file
file_path = os.path.join(save_folder, filename)

with open(file_path, 'r', encoding="utf-8") as file:
            existing_lines = [line.strip() for line in file if line.strip()]
            print(len(existing_lines)) #How many lines there are
            print(type(existing_lines))
            print(f'Starting {existing_lines[0]}') #First line
            print(f'Till {existing_lines[-1]}') #Last line