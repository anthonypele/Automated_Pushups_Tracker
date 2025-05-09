import re
import pandas as pd
import numpy as np 

# Imports from my utilities
from utilities.choose_file import choose_file
from utilities.aliases import aliases

# %% Open a file dialog to choose a file

def excel_and_pivot():
    # Read my txt file
    with open(choose_file(), 'r', encoding="utf-8") as file:
        lines = file.readlines() #creating a list made of each line from the txt imported WA file

    pattern = r"\[(\d{2}\.\d{2}\.\d{4}) (\d{1,2}:\d{2})\] (.*?): (\d+)"

    # New variables
    new_lines = []
    data = []

    # Changing names
 
    def replace_name(match):
        date, time, name, pushups = match.groups()
        new_name = aliases.get(name, name)
        return f'[{date} {time}] {new_name}: {pushups}'

    # Changing my lines
    new_lines = [re.sub(pattern, replace_name, line) for line in lines]

    # Parse lines
    for line in new_lines:
        match = re.match(pattern, line.strip())
        if match:
            date, time, name, pushups = match.groups()
            data.append({
                'date': date,
                'time': time,
                'name': name,
                'pushups': int(pushups)
            })

    # Create a DataFrame 
    df = pd.DataFrame(data)

    # Ensure the date column is treated as data
    df['date'] = pd.to_datetime(df['date'], format="%d.%m.%Y")

    # Create a new column for the month
    df['month'] = df['date'].dt.to_period('M')

    # Create the pivot table
    pivot = pd.pivot_table(
        df,
        index='name',
        columns='month',
        values='pushups',
        aggfunc='sum',
        fill_value=0,
        margins=True,
        margins_name='Итог'
    )

    # Remove the total column, that calculates rows
    pivot = pivot.drop(columns='Итог')

    # Get the list of all month columns in the pivot
    all_months = [col for col in pivot.columns] #if col != 'Итог']
    # Sort them
    all_months_sorted = sorted(all_months)
    # Choose the last 2 months only
    last_two_months = all_months_sorted[-2:]
    # Filter the pivot for only these 2 months
    filtered_pivot = pivot[last_two_months].copy()

    # Create % column to see the difference in %
    division = filtered_pivot[last_two_months[-1]] / filtered_pivot[last_two_months[-2]]
    filtered_pivot['%'] = np.where( # A dance to get rid of division on 0 
        np.isfinite(division), # Condition
        (division - 1).round(2), # If True
        np.nan                      # If False
    )
    # Sort the pivot table the way I want
    if 'Итог' in filtered_pivot.index:
        total_row = filtered_pivot.loc[['Итог']] # Keep as DataFrame
        filtered_pivot = filtered_pivot.drop('Итог')
    else:
        total_row = None
    filtered_pivot = filtered_pivot.sort_values([last_two_months[-1]], ascending=False) 
    if total_row is not None:
        filtered_pivot = pd.concat([filtered_pivot, total_row])

    #pyperclip.copy(filtered_pivot)

    # Creating other pivot table with counts to test it
    # Create the pivot table
    pivot2 = pd.pivot_table(
        df,
        index='name',
        columns='month',
        values='pushups',
        aggfunc='count',
        fill_value=0,
        margins=True,
        margins_name='Итог'
    )

    # Remove the total column, that calculates rows
    pivot2 = pivot2.drop(columns='Итог')
    # Filter the pivot for only these 2 months
    filtered_pivot2 = pivot2[last_two_months].copy()

    # Create % column to see the difference in %
    division = filtered_pivot2[last_two_months[-1]] / filtered_pivot2[last_two_months[-2]]
    filtered_pivot2['%'] = np.where( # A dance to get rid of division on 0 
        np.isfinite(division), # Condition
        (division - 1).round(2), # If True
        np.nan                      # If False
    )
    # Sort the pivot table the way I want
    if 'Итог' in filtered_pivot2.index:
        total_row = filtered_pivot2.loc[['Итог']] # Keep as DataFrame
        filtered_pivot2 = filtered_pivot2.drop('Итог')
    else:
        total_row = None
    filtered_pivot2 = filtered_pivot2.sort_values([last_two_months[-1]], ascending=False)
    if total_row is not None:
        filtered_pivot2 = pd.concat([filtered_pivot2, total_row])
    return df, filtered_pivot, filtered_pivot2
print('it works')