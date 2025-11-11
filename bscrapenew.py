import cloudscraper
from datetime import datetime
import time
import requests

# Barnard scraper setup
scraper = cloudscraper.create_scraper()


URL = "https://apiv4.dineoncampus.com/sites/todays_menu"
params = {
    "siteId": "5cb77d6e4198d40babbc28b5",
}


headers = {
    #"User-Agent": cloudscraper.get_user_agent(browser="chrome"),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://new.dineoncampus.com",
    "Referer": "https://new.dineoncampus.com/barnard",
}

resp = scraper.get(URL, params=params, headers=headers, timeout=30)
resp.raise_for_status()
data = resp.json()
print(data)

"""import re
from collections import defaultdict

_ws = re.compile(r"\s+")

def _clean(s: str | None) -> str:
    if not s:
        return ""
    # collapse weird whitespace (e.g., tabs in "Orange Chicken\t\t")
    return _ws.sub(" ", s).strip()

def parse_menus(
    todays_menu_json: dict,
    *,
    hall_id_map: dict[str, str] | None = None,   # e.g. {"5d8775...":"Diana", ...}
    include_meta: bool = False                   # if True, include (name, calories, portion) tuples
) -> dict:
    result: dict[str, dict] = {}

    for loc in todays_menu_json.get("locations", []):
        loc_id = str(loc.get("id", ""))
        loc_name = _clean(loc.get("name", ""))

        # Filter/rename halls if a map is supplied
        if hall_id_map is not None:
            if loc_id not in hall_id_map:
                continue
            hall_name = hall_id_map[loc_id]
        else:
            hall_name = loc_name or loc_id

        periods_out: dict[str, dict] = {}

        for period in (loc.get("periods") or []):
            p_name = _clean(period.get("name", ""))
            if not p_name:
                # fallback to id if no name
                p_name = str(period.get("id", ""))
            stations_out: dict[str, list] = {}

            for station in (period.get("stations") or []):
                s_name = _clean(station.get("name", "")) or str(station.get("id", ""))
                items_list = []
                seen = set()

                for item in (station.get("items") or []):
                    nm = _clean(item.get("name"))
                    if not nm:
                        continue

                    if include_meta:
                        obj = {
                            "name": nm,
                            "calories": item.get("calories"),
                            "portion": _clean(item.get("portion")),
                        }
                        # Use name+portion as a simple de-dupe key
                        key = (obj["name"], obj["portion"])
                        if key in seen:
                            continue
                        seen.add(key)
                        items_list.append(obj)
                    else:
                        if nm in seen:
                            continue
                        seen.add(nm)
                        items_list.append(nm)

                stations_out[s_name] = items_list

            periods_out[p_name] = stations_out

        # only add halls that have at least one period/station
        result[hall_name] = periods_out

    return result

hall_map = {
    "5d8775484198d40d7a0b8078": "Diana",      # Diana Center Cafe
    "5d27a0461ca48e0aca2a104c": "Hewitt",     # Hewitt Dining
    "5d794b63c4b7ff15288ba3da": "Hewitt Kosher",
}
parsed = parse_menus(data, hall_id_map=hall_map, include_meta=False)
print(parsed)"""