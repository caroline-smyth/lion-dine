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
            4: ["breakfast", "lunch", "dinner"],  # Friday
            5: [],  # Saturday - closed
            6: ["breakfast", "lunch", "dinner"],  # Sunday
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
            4: ["dinner", "latenight"],  # Friday
            5: ["dinner", "latenight"],  # Saturday
            6: [],  # Sunday
        },
        "station_mapping": {
            "breakfast": [],
            "lunch": ["lunch"],
            "dinner": [],
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
        "station_mapping": {
            "breakfast": [],
            "lunch": ["lunch"],
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
            6: [],  # Sunday
        },
        "station_mapping": {
            "breakfast": [],
            "lunch": ["lunch & dinner"],
            "dinner": ["lunch & dinner"],
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

def update_hall_schedule(hall_name: str, weekday: int, meals: List[str]):
    """
    Update the schedule for a specific hall and weekday.
    
    Args:
        hall_name: Name of the dining hall
        weekday: Day of week (0=Monday, 6=Sunday)
        meals: List of meals the hall is open for
    """
    if hall_name in DINING_SCHEDULES:
        DINING_SCHEDULES[hall_name]["schedule"][weekday] = meals

def add_hall_config(hall_name: str, schedule: Dict[int, List[str]], 
                   station_mapping: Dict[str, List[str]]):
    """
    Add a new dining hall configuration.
    
    Args:
        hall_name: Name of the dining hall
        schedule: Schedule dict with weekday as keys and meal lists as values
        station_mapping: Mapping of meals to station types
    """
    DINING_SCHEDULES[hall_name] = {
        "schedule": schedule,
        "station_mapping": station_mapping
    } 