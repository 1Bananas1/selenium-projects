import time

def countdown(seconds):
    """Displays a countdown timer in minutes and seconds."""
    minutes_left = seconds // 60
    seconds_left = seconds % 60
    while seconds > 0:
        print(f"Time remaining: {minutes_left} minutes {seconds_left} seconds")
        time.sleep(1)
        seconds -= 1
        minutes_left = seconds // 60
        seconds_left = seconds % 60
