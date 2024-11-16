import time
def countdown(seconds):
  """Displays a countdown timer in minutes and seconds."""
  minutes_left = seconds // 60
  seconds_left = seconds % 60
  while seconds > 0:
    print(f"\n \n \n Site Down for Maintenance \n \n \n Time remaining: {minutes_left} minutes {seconds_left} seconds \n\n\n\n\n\n")
    time.sleep(1)
    seconds -= 1
    minutes_left = seconds // 60
    seconds_left = seconds % 60