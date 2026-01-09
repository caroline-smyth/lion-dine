from typing import Dict, List, Set, Any
from datetime import datetime

# Dining hall schedules configuration
# Each hall has a schedule dict with weekday (0=Monday, 6=Sunday) as keys
# Each weekday has a list of meals when the hall is open
DINING_SCHEDULES = {
    "John Jay": {
        "schedule": {
            0: ["breakfast", "lunch", "dinner"],  # Monday
            1: ["breakfast", "lunch", "dinner"],  # Tuesday
            2: ["breakfast", "lunch", "dinner"],  # Wednesday
            3: ["breakfast", "lunch", "dinner"],  # Thursday
            4: [],  # Friday - closed
            5: [],  # Saturday - closed
            6: ["breakfast", "lunch", "dinner"],  # Sunday
        },
        "hours": {
            "breakfast": "9:30 AM to 11:00 AM",
            "lunch": "11:00 AM to 2:30 PM",
            "dinner": "5:00 PM to 9:00 PM",
        },
        "station_mapping": {
            "breakfast": ["breakfast", "brunch"],
            "lunch": ["lunch", "lunch & dinner"],
            "dinner": ["dinner", "lunch & dinner"],
            "latenight": []
        }
    },
    "Ferris": {
        "schedule": {
            0: ["breakfast", "lunch", "dinner"],  # Monday
            1: ["breakfast", "lunch", "dinner"],  # Tuesday
            2: ["breakfast", "lunch", "dinner"],  # Wednesday
            3: ["breakfast", "lunch", "dinner"],  # Thursday
            4: ["breakfast", "lunch", "dinner"],  # Friday
            5: ["breakfast", "lunch", "dinner"],  # Saturday
            6: ["breakfast", "lunch", "dinner"],  # Sunday
        },
        "hours": {
            "breakfast": {
                "default": "7:30 AM to 11:00 AM",
                5: "9:00 AM to 11:00 AM",  # Saturday
                6: "10:00 AM to 2:00 PM",  # Sunday 
            },
            "lunch": {
                "default": "11:00 AM to 5:00 PM",
                6: "10:00 AM to 2:00 PM",  # Sunday 
            },
            "dinner": {
                "default": "5:00 PM to 8:00 PM",
                6: "4:00 PM to 8:00 PM",  # Sunday
            },
        },
        "station_mapping": {
            "breakfast": ["breakfast", "brunch"],
            "lunch": ["lunch", "lunch & dinner"],
            "dinner": ["dinner", "lunch & dinner"],
            "latenight": []
        }
    },
    "JJ's": {
        "schedule": {
            0: ["breakfast", "lunch", "dinner", "latenight"],  # Monday
            1: ["breakfast", "lunch", "dinner", "latenight"],  # Tuesday
            2: ["breakfast", "lunch", "dinner", "latenight"],  # Wednesday
            3: ["breakfast", "lunch", "dinner", "latenight"],  # Thursday
            4: ["breakfast", "lunch", "dinner", "latenight"],  # Friday
            5: ["breakfast", "lunch", "dinner", "latenight"],  # Saturday
            6: ["breakfast", "lunch", "dinner", "latenight"],  # Sunday
        },
        "hours": {
            "breakfast": "12:00 AM to 10:00 AM",
            "lunch": "12:00 PM to midnight",
            "dinner": "12:00 PM to midnight",
            "latenight": "Midnight to 10:00 AM",
        },
        "station_mapping": {
            "breakfast": ["breakfast", "daily"],
            "lunch": ["lunch & dinner", "daily"],
            "dinner": ["daily", "lunch & dinner", "late night"],
            "latenight": ["lunch & dinner", "late night"]
        }
    },
    "Johnny's": {
        "schedule": {
            0: ["lunch"],  # Monday
            1: ["lunch"],  # Tuesday
            2: ["lunch"],  # Wednesday
            3: ["lunch", "dinner", "latenight"],  # Thursday
            4: ["lunch", "dinner", "latenight"],  # Friday
            5: ["dinner", "latenight"],  # Saturday
            6: ["dinner", "latenight"],  # Sunday
        },
        "hours": {
            "lunch": "11:00 AM to 2:30 PM",
            "dinner": {
                "default": "7:00 PM to 11:00 PM",
                6: "6:00 PM to 10:00 PM",  # Sunday
            },
            "latenight": {
                "default": "7:00 PM to 11:00 PM",
                6: "6:00 PM to 10:00 PM",  # Sunday
            },
        },
        "station_mapping": {
            "breakfast": [],
            "lunch": ["lunch"],
            "dinner": ["dinner"],
            "latenight": []
        }
    },
    "Hewitt Dining": {
        "schedule": {
            0: ["breakfast", "lunch", "dinner"],  # Monday
            1: ["breakfast", "lunch", "dinner"],  # Tuesday
            2: ["breakfast", "lunch", "dinner"],  # Wednesday
            3: ["breakfast", "lunch", "dinner"],  # Thursday
            4: ["breakfast", "lunch", "dinner"],  # Friday
            5: ["breakfast", "lunch", "dinner"],  # Saturday
            6: ["breakfast", "lunch", "dinner"],  # Sunday
        },
        "hours": {
            "breakfast": {
                "default": "7:30 AM to 10:00 AM",
                5: "10:30 AM to 3:00 PM",  # Saturday (brunch)
                6: "10:30 AM to 3:00 PM",  # Sunday (brunch)
            },
            "lunch": {
                "default": "11:00 AM to 2:30 PM",
                5: "10:30 AM to 3:00 PM",  # Saturday (brunch)
                6: "10:30 AM to 3:00 PM",  # Sunday (brunch)
            },
            "dinner": "4:30 PM to 8:00 PM",
        },
        "station_mapping": {
            "breakfast": ["breakfast", "brunch", "every day"],
            "lunch": ["lunch", "brunch", "every day"],
            "dinner": ["dinner", "every day"],
            "latenight": []
        }
    },
    "Kosher": {
        "schedule": {
            0: ["breakfast", "lunch", "dinner"],  # Monday
            1: ["breakfast", "lunch", "dinner"],  # Tuesday
            2: ["breakfast", "lunch", "dinner"],  # Wednesday
            3: ["breakfast", "lunch", "dinner"],  # Thursday
            4: ["breakfast", "lunch"],  # Friday - no dinner
            5: [],  # Saturday - closed
            6: ["breakfast", "lunch", "dinner"],  # Sunday
        },
        "hours": {
            # TODO: Add Kosher hours when implemented
            "dinner": "4:30 PM to 8:00 PM",
        },
        "station_mapping": {
            "breakfast": ["breakfast"],
            "lunch": ["brunch", "lunch"],
            "dinner": ["brunch", "dinner"],
            "latenight": []
        }
    },
    "Faculty House": {
        "schedule": {
            0: ["lunch"],  # Monday
            1: ["lunch"],  # Tuesday
            2: ["lunch"],  # Wednesday
            3: ["lunch"],  # Thursday
            4: [],  # Friday
            5: [],  # Saturday
            6: [],  # Sunday
        },
        "hours": {
            "lunch": "11:00 AM to 2:30 PM",
        },
        "station_mapping": {
            "breakfast": [],
            "lunch": ["lunch", "lunch & dinner"],
            "dinner": [],
            "latenight": []
        }
    },
    "Chef Mike's": {
        "schedule": {
            0: ["lunch", "dinner"],  # Monday
            1: ["lunch", "dinner"],  # Tuesday
            2: ["lunch", "dinner"],  # Wednesday
            3: ["lunch", "dinner"],  # Thursday
            4: ["lunch", "dinner"],  # Friday
            5: [],  # Saturday
            6: [],  # Sunday
        },
        "hours": {
            "lunch": "10:30 AM to 10:00 PM",
            "dinner": "10:30 AM to 10:00 PM",
        },
        "station_mapping": {
            "breakfast": [],
            "lunch": ["lunch & dinner"],
            "dinner": ["lunch & dinner"],
            "latenight": []
        }
    },
    "Chef Don's": {
        "schedule": {
            0: ["breakfast", "lunch", "dinner"],  # Monday
            1: ["breakfast", "lunch", "dinner"],  # Tuesday
            2: ["breakfast", "lunch", "dinner"],  # Wednesday
            3: ["breakfast", "lunch", "dinner"],  # Thursday
            4: ["breakfast", "lunch", "dinner"],  # Friday
            5: [],  # Saturday
            6: [],  # Sunday
        },
        "hours": {
            "breakfast": "8:00 AM to 11:00 AM",
            "lunch": "11:00 AM to 6:00 PM",
            "dinner": "11:00 AM to 6:00 PM",
        },
        "station_mapping": {
            "breakfast": ["hardcoded_breakfast"],
            "lunch": ["hardcoded_lunch_dinner"],
            "dinner": ["hardcoded_lunch_dinner"],
            "latenight": []
        }
    },
    "Grace Dodge": {
        "schedule": {
            0: ["lunch", "dinner"],  # Monday
            1: ["lunch", "dinner"],  # Tuesday
            2: ["lunch", "dinner"],  # Wednesday
            3: ["lunch", "dinner"],  # Thursday
            4: [],  # Friday
            5: [],  # Saturday
            6: [],  # Sunday
        },
        "hours": {
            "lunch": "11:00 AM to 7:00 PM",
            "dinner": "11:00 AM to 7:00 PM",
        },
        "station_mapping": {
            "breakfast": [],
            "lunch": ["lunch & dinner"],
            "dinner": ["lunch & dinner"],
            "latenight": []
        }
    },
    "Fac Shack": {
        "schedule": {
            0: ["lunch", "dinner"],  # Monday
            1: ["lunch", "dinner"],  # Tuesday
            2: ["lunch", "dinner"],  # Wednesday
            3: ["lunch", "dinner"],  # Thursday
            4: [],  # Friday
            5: [],  # Saturday
            6: ["dinner"],  # Sunday
        },
        "hours": {
            "lunch": "12:00 PM to 4:00 PM",
            "dinner": {
                "default": "4:00 PM to 8:00 PM",
                6: "3:00 PM to 8:00 PM",  # Sunday
            },
        },
        "station_mapping": {
            "breakfast": [],
            "lunch": ["lunch & dinner"],
            "dinner": ["dinner", "lunch & dinner"],
            "latenight": ["lunch & dinner"]
        }
    },
    "Diana": {
        "schedule": {
            0: ["breakfast", "lunch", "dinner", "latenight"],  # Monday
            1: ["breakfast", "lunch", "dinner", "latenight"],  # Tuesday
            2: ["breakfast", "lunch", "dinner", "latenight"],  # Wednesday
            3: ["breakfast", "lunch", "dinner", "latenight"],  # Thursday
            4: ["breakfast", "lunch"],  # Friday - no dinner/latenight
            5: [],  # Saturday
            6: ["lunch", "dinner"],  # Sunday
        },
        "hours": {
            "breakfast": "9:00 AM to 3:00 PM",
            "lunch": {
                "default": "12:00 PM to 3:00 PM",
                6: "12:00 PM to 8:00 PM",  # Sunday
            },
            "dinner": {
                "default": "5:00 PM to 12:00 AM",
                6: "12:00 PM to 8:00 PM",  # Sunday
            },
            "latenight": "8:00 PM to midnight",
        },
        "station_mapping": {
            "breakfast": ["breakfast"],
            "lunch": ["brunch", "lunch"],
            "dinner": ["brunch", "dinner"],
            "latenight": ["late night"]
        }
    }
}

# menu items for halls that don't use scraped data
HARDCODED_MENUS = {
    "Chef Don's": {
        "hardcoded_breakfast": {
            "Sandwiches": ["Bacon egg and cheese bagel", "Ham egg and cheese bagel", "Vegan breakfast bagel"],
            "Sides": ["Cup of oatmeal", "Piece of fruit", "Danish pastry", "Small coffee or tea"]
        },
        "hardcoded_lunch_dinner": {
            "Entree": ["Build your own pizza", "Toasted Cuban sandwich"],
            "Sides": ["Piece of fruit", "Soup", "Milkshake", "Freestyle machine beverage", "Dessert"]
        }
    }
}

def is_hall_open(hall_name: str, weekday: int, meal: str) -> bool:
    """
    Check if a dining hall is open for a specific meal on a given weekday.
    
    Args:
        hall_name: Name of the dining hall
        weekday: Day of week (0=Monday, 6=Sunday)
        meal: Meal period ("breakfast", "lunch", "dinner", "latenight")
    
    Returns:
        True if the hall is open, False otherwise
    """
    if hall_name not in DINING_SCHEDULES:
        return False
    
    schedule = DINING_SCHEDULES[hall_name]["schedule"]
    if weekday not in schedule:
        return False
    
    return meal in schedule[weekday]

def get_station_mapping(hall_name: str, meal: str) -> List[str]:
    """
    Get the station mapping for a hall and meal.
    
    Args:
        hall_name: Name of the dining hall
        meal: Meal period
    
    Returns:
        List of station types to include for this meal
    """
    if hall_name not in DINING_SCHEDULES:
        return []
    
    mapping = DINING_SCHEDULES[hall_name]["station_mapping"]
    return mapping.get(meal, [])

def get_hardcoded_menu(hall_name: str, meal: str) -> Dict[str, List[str]]:
    """
    Get hardcoded menu items for halls that don't use scraped data.
    
    Args:
        hall_name: Name of the dining hall
        meal: Meal period
    
    Returns:
        Dictionary of station names to food items
    """
    if hall_name not in HARDCODED_MENUS:
        return {}
    
    # Map meal to hardcoded menu key
    if meal == "breakfast":
        menu_key = "hardcoded_breakfast"
    elif meal in ["lunch", "dinner"]:
        menu_key = "hardcoded_lunch_dinner"
    else:
        return {}
    
    return HARDCODED_MENUS[hall_name].get(menu_key, {})

def get_all_hall_names() -> List[str]:
    """Get list of all dining hall names."""
    return list(DINING_SCHEDULES.keys())

def get_hall_hours(hall_name: str, meal: str, weekday: int) -> str:
    """
    Get the display hours for a specific hall, meal, and day.
    
    Args:
        hall_name: Name of the dining hall
        meal: Meal period ("breakfast", "lunch", "dinner", "latenight")
        weekday: Day of week (0=Monday, 6=Sunday)
    
    Returns:
        Hours string like "11:00 AM to 2:30 PM" or "Hours not available"
    """
    if hall_name not in DINING_SCHEDULES:
        return "Hours not available"
    
    hours_config = DINING_SCHEDULES[hall_name].get("hours", {})
    meal_hours = hours_config.get(meal)
    
    if meal_hours is None:
        return "Hours not available"
    
    # Simple case: same hours every day
    if isinstance(meal_hours, str):
        return meal_hours
    
    # Complex case: day-specific hours
    if isinstance(meal_hours, dict):
        return meal_hours.get(weekday, meal_hours.get("default", "Hours not available"))
    
    return "Hours not available"

def get_hours_for_meal(weekday: int, meal: str) -> Dict[str, str]:
    """
    Get display hours for all halls for a given meal and weekday.
    
    Main function used by app.py to get hours to display.
    
    Args:
        weekday: Day of week (0=Monday, 6=Sunday)
        meal: Meal period ("breakfast", "lunch", "dinner", "latenight")
    
    Returns:
        Dictionary mapping hall names to their hours strings
    """
    hours = {}
    for hall_name in DINING_SCHEDULES:
        schedule = DINING_SCHEDULES[hall_name]["schedule"]
        
        # Check if hall is open for this meal on this day
        if meal not in schedule.get(weekday, []):
            hours[hall_name] = f"Closed for {meal}"
        else:
            hours[hall_name] = get_hall_hours(hall_name, meal, weekday)
    
    return hours