from datetime import datetime
import pytz
from dining_config import DINING_SCHEDULES, get_all_hall_names

def hours_dict(weekday):
    """
    General hours for all dining halls on a given weekday
    """
    open_hours = {}

    all_halls = get_all_hall_names()
    
    # initialize all halls as closed
    for hall_name in all_halls:
        open_hours[hall_name] = "Closed today"
    
    # set hours based on the configuration and general patterns
    if weekday in [0, 1, 2, 3, 6]:  # Mon-Thu, Sun
        open_hours["John Jay"] = "9:30 AM to 9:00 PM"
    else:
        open_hours["John Jay"] = "Closed today"
    
    # JJ's is open every day
    open_hours["JJ's"] = "12:00 AM to 10:00 AM"
    
    # Ferris - Mon-Fri
    if weekday in [0, 1, 2, 3, 4]:
        open_hours["Ferris"] = "7:30 AM to 8:00 PM"
    elif weekday == 5:  # Saturday
        open_hours["Ferris"] = "9:00 AM to 8:00 PM"
    else:  # Sunday
        open_hours["Ferris"] = "10:00 AM to 2:00 PM, 4:00 PM to 8:00 PM"
    
    # Chef Mike's - Mon-Fri
    if weekday in [0, 1, 2, 3, 4]:
        open_hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
    else:
        open_hours["Chef Mike's"] = "Closed today"
    
    # Chef Don's - Mon-Fri
    if weekday in [0, 1, 2, 3, 4]:
        open_hours["Chef Don's"] = "8:00 AM to 6:00 PM"
    else:
        open_hours["Chef Don's"] = "Closed today"
    
    # Hewitt Dining - varies by day
    if weekday in [0, 1, 2, 3, 4]:
        open_hours["Hewitt Dining"] = "7:30 AM to 10:00 AM, 11:00 AM to 2:30 PM, 4:30 PM to 8:00 PM"
    else:
        open_hours["Hewitt Dining"] = "10:30 AM to 3:00 PM, 4:30 PM to 8:00 PM"
    
    # Faculty House - Mon-Wed
    if weekday in [0, 1, 2]:
        open_hours["Faculty House"] = "11:00 AM to 2:30 PM"
    else:
        open_hours["Faculty House"] = "Closed today"
    
    # Grace Dodge - Mon-Thu
    if weekday in [0, 1, 2, 3]:
        open_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
    else:
        open_hours["Grace Dodge"] = "Closed today"
    
    # Diana - varies by day
    if weekday in [0, 1, 2, 3]:
        open_hours["Diana"] = "9:00 AM to 3:00 PM, 5:00 PM to midnight"
    elif weekday == 4:  # Friday
        open_hours["Diana"] = "9:00 AM to 3:00 PM"
    elif weekday == 6:  # Sunday
        open_hours["Diana"] = "12:00 PM to 8:00 PM"
    else:
        open_hours["Diana"] = "Closed today"
    
    # Johnny's - varies by day
    if weekday in [0, 1, 2, 3]:
        open_hours["Johnny's"] = "11:00 AM to 11:00 PM"
    else:
        open_hours["Johnny's"] = "Closed today"
    
    # Fac Shack - varies by day
    if weekday in [0, 1, 2, 3]:
        open_hours["Fac Shack"] = "11:30 AM to 5:30 PM"
    else:
        open_hours["Fac Shack"] = "Closed today"
    
    # Kosher - varies by day
    if weekday in [0, 1, 2, 3, 6]:
        open_hours["Kosher"] = "4:30 PM to 8:00 PM"
    else:
        open_hours["Kosher"] = "Closed today"
    
    return open_hours

def all_closed(weekday, now):
    """Return all halls as closed - summer break etc"""
    hours = {}
    all_halls = get_all_hall_names()
    for hall in all_halls:
        hours[hall] = "Closed today"
    return hours

def breakfast_hours(weekday, now):
    """Get breakfast hours for all dining halls."""
    b_hours = {}
    all_halls = get_all_hall_names()
    
    # Initialize all halls as closed for breakfast
    for hall_name in all_halls:
        b_hours[hall_name] = "Closed for breakfast"
    
    # Set breakfast hours based on configuration
    if weekday in [6, 0, 1, 2, 3]:  # Sun-Thu
        b_hours["John Jay"] = "9:30 AM to 11:00 AM"
    
    b_hours["JJ's"] = "12:00 AM to 10:00 AM"
    
    if weekday in [0, 1, 2, 3, 4]:  # Mon-Fri
        b_hours["Chef Don's"] = "8:00 AM to 11:00 AM"
        b_hours["Ferris"] = "7:30 AM to 11:00 AM"
        b_hours["Hewitt Dining"] = "7:30 AM to 10:00 AM"
        b_hours["Diana"] = "9:00 AM to 3:00 PM"
    else:
        b_hours["Hewitt Dining"] = "10:30 AM to 3:00 PM"
    
    if weekday == 5:  # Saturday
        b_hours["Ferris"] = "9:00 AM to 11:00 AM"
    elif weekday == 6:  # Sunday
        b_hours["Ferris"] = "10:00 AM to 2:00 PM"
    
    return b_hours

def lunch_hours(weekday, now):
    """Get lunch hours for all dining halls."""
    l_hours = {}
    all_halls = get_all_hall_names()
    
    # Initialize all halls as closed for lunch
    for hall_name in all_halls:
        l_hours[hall_name] = "Closed for lunch"
    
    # Set lunch hours based on configuration
    l_hours["JJ's"] = "12:00 PM to midnight"
    
    if weekday in [0, 1, 2, 3, 4]:  # Mon-Fri
        l_hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
        l_hours["Chef Don's"] = "11:00 AM to 6:00 PM"
        l_hours["Ferris"] = "11:00 AM to 5:00 PM"
        l_hours["Hewitt Dining"] = "11:00 AM to 2:30 PM"
        l_hours["Diana"] = "12:00 PM to 3:00 PM"
    else:
        l_hours["Hewitt Dining"] = "10:30 AM to 3:00 PM"
        if weekday == 5:  # Saturday
            l_hours["Ferris"] = "11:00 AM to 5:00 PM"
        elif weekday == 6:  # Sunday
            l_hours["Ferris"] = "10:00 AM to 2:00 PM"
            l_hours["Diana"] = "12:00 PM to 8:00 PM"
    
    if weekday in [0, 1, 2]:  # Mon-Wed
        l_hours["Faculty House"] = "11:00 AM to 2:30 PM"
    
    if weekday in [0, 1, 2, 3]:  # Mon-Thu
        l_hours["Fac Shack"] = "11:30 AM to 7:00 PM"
        l_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
        l_hours["Johnny's"] = "11:00 AM to 2:00 PM"
    
    if weekday in [6, 0, 1, 2, 3]:  # Sun-Thu
        l_hours["John Jay"] = "11:00 AM to 2:30 PM"
    
    return l_hours

def dinner_hours(weekday, now):
    """Get dinner hours for all dining halls."""
    d_hours = {}
    all_halls = get_all_hall_names()
    
    # Initialize all halls as closed for dinner
    for hall_name in all_halls:
        d_hours[hall_name] = "Closed for dinner"
    
    # Set dinner hours based on configuration
    d_hours["JJ's"] = "12:00 PM to midnight"
    d_hours["Hewitt Dining"] = "4:30 PM to 8:00 PM"
    d_hours["Ferris"] = "5:00 PM to 8:00 PM"
    
    if weekday in [0, 1, 2, 3, 6]:  # Mon-Thu, Sun
        d_hours["Kosher"] = "4:30 PM to 8:00 PM"
    
    if weekday in [0, 1, 2, 3, 4]:  # Mon-Fri
        d_hours["Chef Mike's"] = "10:30 AM to 10:00 PM"
        d_hours["Chef Don's"] = "11:00 AM to 6:00 PM"
    
    if weekday in [0, 1, 2, 3]:  # Mon-Thu
        d_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
        d_hours["Diana"] = "5:00 PM to 12:00 AM"
        d_hours["Fac Shack"] = "4:00 PM to 7:00 PM"
    elif weekday == 6:  # Sunday
        d_hours["Diana"] = "12:00 PM to 8:00 PM"
    
    if weekday in [6, 0, 1, 2, 3]:  # Sun-Thu
        d_hours["John Jay"] = "5:00 PM to 9:00 PM"
    
    if weekday >= 3 and weekday < 6:  # Thu-Sat
        d_hours["Johnny's"] = "7:00 PM to 11:00 PM"
    
    return d_hours

def latenight_hours(weekday, now):
    """Get late night hours for all dining halls."""
    ln_hours = {}
    all_halls = get_all_hall_names()
    
    # Initialize all halls as closed for late night
    for hall_name in all_halls:
        ln_hours[hall_name] = "Closed for late night"
    
    # Set late night hours based on configuration
    ln_hours["JJ's"] = "Midnight to 10:00 AM"
    
    if weekday in [0, 1, 2, 3]:  # Mon-Thu
        ln_hours["Diana"] = "8:00 PM to midnight"
    
    if weekday >= 3 and weekday < 6:  # Thu-Sat
        ln_hours["Johnny's"] = "7:00 PM to 11:00 PM"
    
    # Special holiday closures
    if now.month == 1 and now.day < 21:  # Christmas break
        ln_hours["JJ's"] = "Closed for late night"
        ln_hours["Diana"] = "Closed for late night"
        ln_hours["Fac Shack"] = "Closed for late night"
        ln_hours["Johnny's"] = "Closed for late night"
    
    return ln_hours