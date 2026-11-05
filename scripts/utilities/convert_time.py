import datetime
from utilities.timezones import get_my_timezone
from utilities.timezones import timezones
from utilities.timezones import timezone_rules

def get_timezone_for_date(pusher_name, date_obj): # This function checks for special rules in timezones dict
    rules = timezone_rules.get(pusher_name)
    if rules:
        for start, end, tz in rules:
            if (start is None or date_obj >= start) and (end is None or date_obj < end):
                return tz
    # Fallback to static timezone if no rule found
    return timezones.get(pusher_name, get_my_timezone())


def convert_time(date_str, time_str, pusher_name): 
    # Parse datetime from string (assumed in my timezone originally)
    naive_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")

    # Attach my timezone to that naive datetime
    my_timezone = get_my_timezone()
    my_dt = naive_dt.replace(tzinfo=my_timezone)

    # Get pusher timezone
    pusher_tz = get_timezone_for_date(pusher_name, naive_dt)

    # Convert from my time to pusher's time
    pusher_dt = my_dt.astimezone(pusher_tz)

    # Return formatted date and time
    return pusher_dt.strftime("%d.%m.%Y"), pusher_dt.strftime("%H:%M")