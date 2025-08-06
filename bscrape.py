import cloudscraper
from datetime import datetime

# Barnard scraper setup
scraper = cloudscraper.create_scraper()

location_ids = {"5d27a0461ca48e0aca2a104c": "Hewitt", "5d794b63c4b7ff15288ba3da": "Hewitt Kosher", "5d8775484198d40d7a0b8078": "Diana"}
dining_hall_data = {}
date = datetime.now().date().isoformat()
base = "https://api.dineoncampus.com/v1/location"
dining_hall_data = {}

# extract meal periods and menu items
def bscrape():
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
      print("Closed")
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

  print(dining_hall_data)


if __name__ == '__main__':
  bscrape() # add a retry for if it fails