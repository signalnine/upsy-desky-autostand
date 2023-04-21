import requests
import time
import arrow
from datetime import timedelta
from ics import Calendar

# Configuration
IP_ADDRESS = "YOUR_UPSY_DESKY_IP"
STANDING_HEIGHT = 41.5
SITTING_HEIGHT = 30.3
TARGET_STANDING_TIME_PER_DAY = 2  # Hours
MAX_STANDING_TIME = 20   # Minutes
SITTING_BREAK_TIME = 20  # Minutes
WORKDAY_HOURS = 8
ICAL = 'https://calendar.google.com/calendar/ical/YOURNAME%40gmail.com/public/basic.ics'
INTERVAL = 60  # Interval between height checks, in seconds

# Fetch the calendar data
def get_calendar():
    response = requests.get(ICAL)
    calendar = Calendar(response.text)
    return calendar

# Check if there's an ongoing event
def is_event_ongoing():
    now = arrow.get(time.time())
    calendar = get_calendar()
    return any(event.begin <= now <= event.end for event in calendar.events)

# Get the current desk height
def get_current_desk_height():
    response = requests.get(f'http://{IP_ADDRESS}/sensor/desk_height')
    data = response.json()
    return float(data["value"])

# Set the desk height
def set_desk_height(value):
    url = f"http://{IP_ADDRESS}/number/target_desk_height/set?value={value}"
    requests.post(url)

def main():
    # Convert time values to seconds
    target_standing_time = TARGET_STANDING_TIME_PER_DAY * 60 * 60
    workday_seconds = WORKDAY_HOURS * 60 * 60
    max_standing_time_at_stretch = MAX_STANDING_TIME * 60
    sitting_break_time = SITTING_BREAK_TIME * 60

    end_time = time.time() + workday_seconds
    last_height_change_time = time.time()
    total_standing_time = 0
    total_sitting_time = 0

    # Main loop
    while time.time() < end_time:
        # Check if there's an ongoing event
        if not is_event_ongoing():
            current_desk_height = get_current_desk_height()
            time_since_last_change = time.time() - last_height_change_time

            # If the desk is at standing height
            if current_desk_height == STANDING_HEIGHT:
                # Check if it's time to switch to sitting height
                if time_since_last_change >= max_standing_time_at_stretch:
                    total_standing_time += max_standing_time_at_stretch
                    set_desk_height(SITTING_HEIGHT)
                    last_height_change_time = time.time()

            # If the desk is at sitting height
            elif current_desk_height == SITTING_HEIGHT:
                total_sitting_time += time_since_last_change

                # Check if it's time to switch to standing height
                if time_since_last_change >= sitting_break_time:
                    if total_standing_time < target_standing_time:
                        set_desk_height(STANDING_HEIGHT)
                        last_height_change_time = time.time()

        # Sleep for the configured interval
        time.sleep(INTERVAL)

    if total_standing_time >= target_standing_time:
        total_standing_time_min = total_standing_time / 60
        total_sitting_time_min = total_sitting_time / 60
        print("Target standing time reached.")
        print(f"Time standing: {total_standing_time_min}")
        print(f"Time sitting: {total_sitting_time_min}")

if __name__ == "__main__":
    main()
