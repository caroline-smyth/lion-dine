import cloudscraper
from datetime import datetime
import time
import requests

# Barnard scraper setup
scraper = cloudscraper.create_scraper()

location_ids = {"5d27a0461ca48e0aca2a104c": "Hewitt Dining", "5d794b63c4b7ff15288ba3da": "Hewitt Kosher", "5d8775484198d40d7a0b8078": "Diana"}
dining_hall_data = {}
date = datetime.now().date().isoformat()
base = "https://api.dineoncampus.com/v1/location"
dining_hall_data = {}

# extract meal periods and menu items with retry functionality
def bscrape(max_retries=3, retry_delay=2):
    for attempt in range(max_retries):
      try:
        # reset dining hall data for each attempt
        dining_hall_data = {}
        
        for location_id in location_ids:
            periods_url = f"{base}/{location_id}/periods"
            params = {"platform": 0, "date": date}
            resp = scraper.get(periods_url, params=params, timeout=30)
            resp.raise_for_status()
            periods = resp.json().get("periods", [])
            hall_name = location_ids[location_id]
            # populate hall data with hall name
            dining_hall_data[hall_name] = {}
            # check if dining hall is closed this day (not hour specific)
            closed = resp.json().get("closed", False)
            if closed:
                print(f"{hall_name} is closed")
                continue

            for p in periods:
                pid, pname = p["id"], p["name"]
                # populate hall data with meal period name
                dining_hall_data[hall_name][pname] = {}
                menu_url = f"{base}/{location_id}/periods/{pid}"
                menu = scraper.get(menu_url, params=params, timeout=30).json()
                cats = menu["menu"]["periods"]["categories"]
                for station in cats:
                    # populate meal period data with station name
                    dining_hall_data[hall_name][pname][station["name"]] = []
                    for item in station["items"]:
                        # populate station data with item name
                        dining_hall_data[hall_name][pname][station["name"]].append(item["name"])

        print("Barnard scraping completed successfully")
        return dining_hall_data
        
      except (requests.exceptions.RequestException, 
              requests.exceptions.Timeout, 
              requests.exceptions.ConnectionError, 
              cloudscraper.exceptions.CloudflareChallengeError,
              KeyError, 
              ValueError) as e:
          print(f"Attempt {attempt + 1} failed: {str(e)}")
          
          if attempt < max_retries - 1:
              print(f"Retrying in {retry_delay} seconds...")
              time.sleep(retry_delay)
              retry_delay *= 2
          else:
              print(f"All {max_retries} attempts failed. Unable to scrape Barnard data.")
              return {hall_name: {} for hall_name in location_ids.values()}

def normalize_meals(halls):
    fixed = {}
    for hall, meals in halls.items():
        if not isinstance(meals, dict):
            fixed[hall] = meals
            continue
        fixed[hall] = { (m.strip().lower()): v for m, v in meals.items() }
    return fixed

if __name__ == '__main__':
  data = bscrape()
  normalized = normalize_meals(data)
  print(normalized)