"""
Time-based functions for handling dining hall hours

Regular semester hours are defined in dining_config.py under each hall's "hours" key
This file handles special schedule overrides for breaks (winter, summer, NSOP, etc)
"""

from datetime import datetime
from typing import Dict, Optional
from dining_config import DINING_SCHEDULES, get_all_hall_names, get_hours_for_meal


# =============================================================================
# BREAK SCHEDULE OVERRIDES
# =============================================================================
# These override regular hours during special periods.
# To activate break schedule, change the function called in app.py
# =============================================================================

def winter_hours(weekday: int, now: datetime) -> Dict[str, str]:
    """
    Winter break hours
    """
    hours = {}
    all_halls = get_all_hall_names()
    
    # Default all halls to closed
    for hall in all_halls:
        hours[hall] = "Closed for winter break"
    
    # 2025-26 schedule
    month = now.month
    day = now.day
    
    if month == 12:
        # Dec 20-31 (excluding Dec 24-25)
        if 20 <= day <= 31 and day not in [24, 25]:
            hours["John Jay"] = "11:00 AM to 2:30 PM, 4:00 PM to 7:00 PM"
    
    if month == 1:
        if 2 <= day <= 10:
            # Jan 2-10: John Jay open
            hours["John Jay"] = "11:00 AM to 2:30 PM, 4:00 PM to 7:00 PM"
        elif 11 <= day <= 15:
            # Jan 11-15: JJ's open
            hours["JJ's"] = "11:00 AM to 7:00 PM"
        elif 16 <= day <= 19:
            # Jan 16-19: Ferris open
            hours["Ferris"] = "11:00 AM to 7:00 PM"
    
    return hours


def nsop_hours(weekday: int, now: datetime) -> Dict[str, str]:
    """
    NSOP hours
    """
    hours = {}
    all_halls = get_all_hall_names()
    for hall in all_halls:
        hours[hall] = "Closed for summer"
    
    # NSOP schedule - update as needed
    hours["John Jay"] = "9:30 AM to 9:00 PM"
    hours["Ferris"] = "9:00 AM to 8:00 PM"
    hours["Johnny's"] = "11:00 AM to 2:30 PM"
    hours["JJ's"] = "12:00 PM to 8:00 PM"
    hours["Hewitt Dining"] = "11:00 AM to 8:00 PM"
    
    return hours


def all_closed(weekday: int, now: datetime) -> Dict[str, str]:
    """
    Summer break
    """
    hours = {}
    all_halls = get_all_hall_names()
    for hall in all_halls:
        hours[hall] = "Closed for summer"
    return hours


# =============================================================================
# TYPICAL SEMESTER HOURS
# =============================================================================
# These functions pull from dining_config.py and are used during the regular semester
# They're wrappers for backwards compatibility with app.py
# =============================================================================

def breakfast_hours(weekday: int, now: datetime) -> Dict[str, str]:
    """Get breakfast hours for all dining halls from dining_config.py"""
    return get_hours_for_meal(weekday, "breakfast")


def lunch_hours(weekday: int, now: datetime) -> Dict[str, str]:
    """Get lunch hours for all dining halls."""
    return get_hours_for_meal(weekday, "lunch")


def dinner_hours(weekday: int, now: datetime) -> Dict[str, str]:
    """Get dinner hours for all dining halls."""
    return get_hours_for_meal(weekday, "dinner")


def latenight_hours(weekday: int, now: datetime) -> Dict[str, str]:
    """Get late night hours for all dining halls."""
    return get_hours_for_meal(weekday, "latenight")
