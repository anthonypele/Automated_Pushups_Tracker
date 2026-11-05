#%% Imports
import re
import datetime
from collections import defaultdict
import os
import pyperclip
import time
import pyautogui as pag

# Imports from my Utilities
from utilities.aliases import aliases
from utilities.choose_file import choose_file


# =========================
# 1) Read the merged pushups log file
# =========================

file_path = choose_file()
with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()


# =========================
# 2) Define date ranges
# =========================

today = datetime.date.today()


def get_monday(date_value):
    return date_value - datetime.timedelta(days=date_value.weekday())


def ask_report_week(today):
    current_week_start = get_monday(today)

    options = {
        "1": (
            "last completed week",
            current_week_start - datetime.timedelta(days=7),
        ),
        "2": (
            "this calendar week",
            current_week_start,
        ),
    }

    print("\nWhich week do you want to analyze?")
    print(
        f"1 - Last completed week: "
        f"{options['1'][1]} to {options['1'][1] + datetime.timedelta(days=6)}"
    )
    print(
        f"2 - This calendar week: "
        f"{options['2'][1]} to {options['2'][1] + datetime.timedelta(days=6)}"
    )
    print("3 - Custom week start date (YYYY-MM-DD, must be Monday)")

    while True:
        choice = input("Choose 1, 2, or 3 [default: 1]: ").strip() or "1"

        if choice in options:
            label, report_week_start = options[choice]
            break

        if choice == "3":
            date_text = input("Enter Monday start date (YYYY-MM-DD): ").strip()
            try:
                report_week_start = datetime.datetime.strptime(
                    date_text, "%Y-%m-%d"
                ).date()
            except ValueError:
                print("Invalid date. Example: 2026-07-06")
                continue

            if report_week_start.weekday() != 0:
                print("That date is not a Monday. Please enter a Monday.")
                continue

            label = "custom week"
            break

        print("Invalid choice. Please choose 1, 2, or 3.")

    report_week_end = report_week_start + datetime.timedelta(days=6)
    previous_week_start = report_week_start - datetime.timedelta(days=7)
    previous_week_end = report_week_start - datetime.timedelta(days=1)

    print(
        f"\nAnalyzing {label}: {report_week_start} to {report_week_end}"
        f"\nComparing with: {previous_week_start} to {previous_week_end}\n"
    )

    return report_week_start, report_week_end, previous_week_start, previous_week_end


(
    start_of_last_week,
    end_of_last_week,
    start_of_week_before_last,
    end_of_week_before_last,
) = ask_report_week(today)


# =========================
# 3) Storage for totals and day counts
# =========================

totals_last_week = defaultdict(int)
totals_week_before_last = defaultdict(int)

# NOTE: This counts "days with at least one record" only if your file has
# at most one line per (date,name). If you have multiple lines per day/person,
# this will count multiple times. (Same behavior as your original script.)
days_count_last_week = defaultdict(int)
days_count_week_before_last = defaultdict(int)


# =========================
# 4) Regex to parse lines
# Supports both:
#   [DD.MM.YYYY HH:MM] Name: N
#   [DD.MM.YYYY HH:MM] [tg] Name: N
#   [DD.MM.YYYY HH:MM] [wa] Name: N
# =========================

pattern = re.compile(
    r"^\[(\d{2}\.\d{2}\.\d{4})\s+\d{1,2}:\d{2}\]\s+(?:\[\w+\]\s+)?(.+?):\s+(\d+)\s*$"
)
# groups:
# 1) date_str "DD.MM.YYYY"
# 2) name (WITHOUT [tg]/[wa] because we ignore that optional tag)
# 3) pushups number


# =========================
# 5) Parse file and aggregate stats
# =========================

for line in lines:
    match = pattern.search(line)
    if not match:
        continue

    date_str, name, pushups = match.groups()

    # Convert date (we ignore time for weekly grouping)
    date = datetime.datetime.strptime(date_str, "%d.%m.%Y").date()

    # Convert pushups to int
    pushups = int(pushups)

    # Normalize display name using aliases dictionary (if exists)
    display_name = aliases.get(name, name)

    # Add to the correct week bucket
    if start_of_last_week <= date <= end_of_last_week:
        totals_last_week[display_name] += pushups
        days_count_last_week[display_name] += 1

    elif start_of_week_before_last <= date <= end_of_week_before_last:
        totals_week_before_last[display_name] += pushups
        days_count_week_before_last[display_name] += 1


# =========================
# 6) Prepare a combined set of all names
# =========================

all_names = set(totals_last_week) | set(totals_week_before_last)


# =========================
# 7) Helper: print + collect output (for clipboard and saving)
# =========================

output_text = ""

def print_and_save(text: str):
    global output_text
    print(text)
    output_text += text + "\n"


# =========================
# 8) Compute differences vs previous week
# =========================

diff_pushups = {}
for name in all_names:
    last = totals_last_week.get(name, 0)
    prev = totals_week_before_last.get(name, 0)
    diff_pushups[name] = last - prev

diff_days = {}
for name in all_names:
    last = days_count_last_week.get(name, 0)
    prev = days_count_week_before_last.get(name, 0)
    diff_days[name] = last - prev


# =========================
# 9) Print summary
# =========================

print_and_save(
    f"\n*Всего отжиманий на прошлой неделе с {start_of_last_week} по {end_of_last_week}:*\n"
    #f"(Посмотреть красивую диаграмму здесь https://public.tableau.com/app/profile/anton.pelepelin/viz/Pushups_data/Dashboard6w :\n"
)

for name in sorted(all_names, key=lambda n: totals_last_week.get(n, 0), reverse=True):
    last_week = totals_last_week.get(name, 0)

    if diff_pushups.get(name, 0) > 0:
        print_and_save(f"{name}: {last_week}, это больше на {diff_pushups[name]}, чем на неделе до 💪")
    elif diff_pushups.get(name, 0) < 0:
        print_and_save(f"{name}: {last_week}, это меньше на {abs(diff_pushups[name])}, чем на неделе до 😴")
    else:
        print_and_save(f"{name}: {last_week}, ровно 😎")


print_and_save("\n*Дней отжиманий за неделю:*\n")

for name in sorted(
    all_names,
    key=lambda x: (days_count_last_week.get(x, 0), days_count_week_before_last.get(x, 0)),
    reverse=True
):
    last_days = days_count_last_week.get(name, 0)
    prev_days = days_count_week_before_last.get(name, 0)

    if last_days == prev_days:
        print_and_save(
            f"{name}: {last_days} дн., неделю назад - {prev_days} дн. Стабильность - признак мастерства"
        )
    else:
        print_and_save(f"{name}: {last_days} дн., неделю назад - {prev_days} дн.")


# =========================
# 10) Copy output to clipboard + save message file
# =========================

pyperclip.copy(output_text)

base_folder = r"C:\Users\Anthony\YandexDisk\_Programming\APT\Data"
messages_folder = os.path.join(base_folder, "Messages")
os.makedirs(messages_folder, exist_ok=True)

message_file = f"{start_of_last_week} - {end_of_last_week} Message.txt"
message_file_path = os.path.join(messages_folder, message_file)

with open(message_file_path, "w", encoding="utf-8") as file:
    file.write(output_text)


# =========================
# 11) Open WhatsApp and prepare paste (your existing automation)
# =========================
"""
pag.hotkey("win", "s")
time.sleep(2)
pyperclip.copy("Whatsapp")
pag.hotkey("ctrl", "v")
time.sleep(0.1)
pag.press("enter")
time.sleep(3)
pag.press("esc")

# Search for the group
pag.hotkey("ctrl", "f")
time.sleep(1)
group_name = "Кто отжимается по утрам"
pyperclip.copy(group_name)
pag.hotkey("ctrl", "a")
pag.hotkey("ctrl", "v")
time.sleep(1)
pag.hotkey("down")
time.sleep(1)
pag.press("enter")
time.sleep(2)

# Paste message (waiting for your manual Enter)
pyperclip.copy(output_text)
pag.hotkey("ctrl", "v")
"""
