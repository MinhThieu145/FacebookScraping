from datetime import datetime, timedelta

def print_recurring_times(hour, minute):
    # Set the initial datetime to today at 12 AM
    dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Create a time object for the given hour and minute
    time_obj = datetime.strptime(f'{hour}:{minute}', '%H:%M').time()

    # Loop until the next day at 12 AM
    while dt < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1):
        # Combine the date and time to form a datetime object
        dt_with_time = datetime.combine(dt.date(), time_obj)

        # Format and print the time
        print(dt_with_time.strftime('%I:%M%p'))

        # Add the given hour and minute to the current datetime
        
        time_obj += timedelta(hours=hour, minutes=minute)
        dt += timedelta(hours=hour, minutes=minute)

print_recurring_times(1, 30)