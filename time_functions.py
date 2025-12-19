from datetime import datetime
import pytz
from dining_config import DINING_SCHEDULES, get_all_hall_names

def nsop_hours(weekday, now):
    hours = {}
    all_halls = get_all_hall_names()
    
    for hall in all_halls:
        hours[hall] = "Closed for summer"
    hours["John Jay"] = "9:30 AM to 9:00 PM"
    hours["Ferris"] = "9:00 AM to 8:00 PM"
    hours["Johnny's"] = "11:00 AM to 2:30 PM"
    hours["JJ's"] = "12:00 PM to 8:00 PM"
    hours["Hewitt Dining"] = "11:00 AM to 8:00 PM"
    
    return hours

def winter_hours(weekday, now):
    hours = {}
    all_halls = get_all_hall_names()
    for hall in all_halls:
        hours[hall] = "Closed for winter break"

    if datetime.now().month == 12:
        if datetime.now().day <= 31 and datetime.now().day >= 20 and datetime.now().day != 4 and datetime.now().day != 25:
            hours["John Jay"] = "11:00 AM to 2:30 PM, 4:00 PM to 7:00 PM"
    if datetime.now().month == 1:
        if datetime.now().day <= 10 and datetime.now().day >= 2:
            hours["John Jay"] = "11:00 AM to 2:30 PM, 4:00 PM to 7:00 PM"
        elif datetime.now().day <= 15 and datetime.now().day >= 11:
            hours["JJ's"] = "11:00 AM to 7:00 PM"
        elif datetime.now().day <= 19 and datetime.now().day >= 16:
            hours["Ferris"] = "11:00 AM to 7:00 PM"
    return hours

def all_closed(weekday, now):
    """Return all halls as closed - summer break etc"""
    hours = {}
    all_halls = get_all_hall_names()
    for hall in all_halls:
        hours[hall] = "Closed for summer"
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
    
    if weekday in [0, 1, 2, 3]:  # Mon-Thu
        l_hours["Fac Shack"] = "12:00 PM to 4:00 PM"
        l_hours["Grace Dodge"] = "11:00 AM to 7:00 PM"
        l_hours["Johnny's"] = "11:00 AM to 2:30 PM"
        l_hours["Faculty House"] = "11:00 AM to 2:30 PM"
    
    if weekday in [6, 0, 1, 2, 3]:  # Sun-Thu
        l_hours["John Jay"] = "11:00 AM to 2:30 PM"

    l_hours["Johnny's"] = "Closed for lunch"
    
    return l_hours

def dinner_hours(weekday, now):
    """Get dinner hours for all dining halls."""
    d_hours = {}
    all_halls = get_all_hall_names()
    
    # Initialize all halls as closed for dinner
    for hall_name in all_halls:
        d_hours[hall_name] = "Closed for dinner"
    
    # Whole week
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
        d_hours["Fac Shack"] = "4:00 PM to 8:00 PM"
    elif weekday == 6:  # Sunday
        d_hours["Diana"] = "12:00 PM to 8:00 PM"
        d_hours["Fac Shack"] = "3:00 PM to 8:00 PM"
        d_hours["Johnny's"] = "6:00 PM to 10:00 PM"
    
    if weekday in [6, 0, 1, 2, 3]:  # Sun-Thu
        d_hours["John Jay"] = "5:00 PM to 9:00 PM"
    
    if weekday >= 3 and weekday < 6:  # Thu-Sat
        d_hours["Johnny's"] = "7:00 PM to 11:00 PM"
    
    d_hours["Johnny's"] = "Closed for dinner"
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
    
    
    return ln_hours