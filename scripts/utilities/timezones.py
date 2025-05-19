import pytz
import tzlocal
import datetime

# Get your current time zone automatically 
def get_my_timezone():
    my_timezone = tzlocal.get_localzone()
    return my_timezone
    print("your local time:", datetime.datetime.now(my_timezone))
    print("your local time zone", my_timezone)

my_timezone = get_my_timezone()
timezones = {
    "Michael Ice&Fire Perm": pytz.timezone('Europe/Madrid'),
    "Anthony": my_timezone,
    "Гриша Соловьев": pytz.timezone('Europe/Moscow'),
    "Павел Антонюк РТ": pytz.timezone('Europe/Moscow'),
    "Андрей Палыч Павлов": pytz.timezone('America/Mexico_City'),
    "Роман Аландаров": pytz.timezone('Europe/Moscow'),
    "Андрей Русанов": pytz.timezone('Europe/Moscow'),
    "Анна Русанова РТ": pytz.timezone('Europe/Moscow'),
    "Аленка Сестренка": pytz.timezone('Europe/Moscow'),
    "Дима Подгузов": pytz.timezone('Europe/Moscow'),
    
}

timezone_rules = {
    "Anthony": [
        # (start_date, end_date, timezone)
        (None, datetime.datetime(2024, 3, 12), pytz.timezone('Europe/Moscow')),
    ],
    "Michael Ice&Fire Perm": [
        (None, None, pytz.timezone('Europe/Madrid'))
    ]
}