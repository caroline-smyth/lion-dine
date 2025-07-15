import sys
from dining_config import DINING_SCHEDULES, update_hall_schedule, add_hall_config

def print_hall_schedule(hall_name):
    """print schedule for specific hall"""
    if hall_name not in DINING_SCHEDULES:
        print(f"Hall '{hall_name}' not found in configuration.")
        return
    
    print(f"\nSchedule for {hall_name}:")
    print("=" * 50)
    
    schedule = DINING_SCHEDULES[hall_name]["schedule"]
    station_mapping = DINING_SCHEDULES[hall_name]["station_mapping"]
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for i, day in enumerate(days):
        meals = schedule.get(i, [])
        if meals:
            print(f"{day:10}: {', '.join(meals)}")
        else:
            print(f"{day:10}: Closed")
    
    print(f"\nStation mappings:")
    for meal, stations in station_mapping.items():
        if stations:
            print(f"  {meal:10}: {', '.join(stations)}")
        else:
            print(f"  {meal:10}: No stations")

def list_all_halls():
    """list all dining halls in the configuration"""
    print("Available dining halls:")
    print("=" * 30)
    for hall_name in sorted(DINING_SCHEDULES.keys()):
        print(f"  - {hall_name}")

def update_schedule_interactive():
    """Interactive function to update a hall's schedule."""
    list_all_halls()
    
    hall_name = input("\nEnter hall name to update: ").strip()
    if hall_name not in DINING_SCHEDULES:
        print(f"Hall '{hall_name}' not found.")
        return
    
    print_hall_schedule(hall_name)
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meals = ["breakfast", "lunch", "dinner", "latenight"]
    
    print(f"\nAvailable meals: {', '.join(meals)}")
    print("Enter 'closed' to mark a day as closed, or 'skip' to keep current schedule")
    
    for i, day in enumerate(days):
        current_meals = DINING_SCHEDULES[hall_name]["schedule"].get(i, [])
        print(f"\n{day} (currently: {', '.join(current_meals) if current_meals else 'Closed'})")
        
        user_input = input("Enter meals (comma-separated) or 'closed': ").strip().lower()
        
        if user_input == 'skip':
            continue
        elif user_input == 'closed':
            update_hall_schedule(hall_name, i, [])
        else:
            new_meals = [meal.strip() for meal in user_input.split(',')]
            # Validate meals
            invalid_meals = [meal for meal in new_meals if meal not in meals]
            if invalid_meals:
                print(f"Invalid meals: {', '.join(invalid_meals)}. Skipping this day.")
                continue
            update_hall_schedule(hall_name, i, new_meals)
    
    print(f"\nUpdated schedule for {hall_name}:")
    print_hall_schedule(hall_name)

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_dining_config.py list                    - List all halls")
        print("  python manage_dining_config.py show <hall_name>        - Show hall schedule")
        print("  python manage_dining_config.py update                  - Interactive update")
        print("  python manage_dining_config.py show-all                - Show all schedules")
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_all_halls()
    
    elif command == "show":
        if len(sys.argv) < 3:
            print("Please provide a hall name.")
            return
        hall_name = sys.argv[2]
        print_hall_schedule(hall_name)
    
    elif command == "show-all":
        for hall_name in sorted(DINING_SCHEDULES.keys()):
            print_hall_schedule(hall_name)
    
    elif command == "update":
        update_schedule_interactive()
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'list', 'show <hall_name>', 'show-all', or 'update'")

if __name__ == "__main__":
    main() 