import json
from typing import Dict, List, Any
try:
    import cloudscraper
except Exception:
    cloudscraper = None
import requests

BARNARD_SITE_ID = "5cb77d6e4198d40babbc28b5"
API_URL = "https://apiv4.dineoncampus.com/sites/todays_menu"

DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    # Use the Barnard frontend pages as origin/referer (these match how real browsers hit the API)
    "Origin": "https://new.dineoncampus.com",
    "Referer": "https://new.dineoncampus.com/barnard",
}
#  location ids -> display names
HALL_ID_TO_NAME = {
    # Diana Center Cafe
    "5d8775484198d40d7a0b8078": "Diana",
    # Hewitt
    "5d27a0461ca48e0aca2a104c": "Hewitt Dining",
    # Hewitt Kosher
    #5d794b63c4b7ff15288ba3da": "Hewitt Kosher",
}

# map API period names to our keys
PERIOD_NAME_MAP = {
    "Breakfast": "breakfast",
    "Brunch": "brunch",
    "Lunch": "lunch",
    "Dinner": "dinner",
    "Late Night": "late night",
    "Daily": "every day",
}

def _get_session():
    # cloudscraper handles Cloudflare; fall back to requests if unavailable
    if cloudscraper is not None:
        return cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'linux', 'mobile': False}, headers=DEFAULT_HEADERS)

        #return cloudscraper.create_scraper()
    return requests.Session()

def _fetch_barnard_raw() -> Dict[str, Any]:
    sess = _get_session()
    resp = sess.get(API_URL, params={"siteId": BARNARD_SITE_ID}, timeout=30)
    resp.raise_for_status()
    return resp.json()

def _extract_items(station: Dict[str, Any]) -> List[str]:
    # convert a station's "items" list of dicts -> list[str] of names
    items = station.get("items") or []
    out: List[str] = []
    for it in items:
        name = (it.get("name") or "").strip()
        if name:
            out.append(name)
    return out

def parse_barnard_to_columbia_shape(data: Dict[str, Any]) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    """
    Parse the DineOnCampus payload into the Lion Dine shape used for Columbia halls.
    """
    result: Dict[str, Dict[str, Dict[str, List[str]]]] = {}
    for loc in data.get("locations", []):
        hall_id = loc.get("id")
        hall_name = HALL_ID_TO_NAME.get(hall_id)
        if not hall_name:
            # skip locations we don't display
            continue

        hall_periods: Dict[str, Dict[str, List[str]]] = {}
        for period in (loc.get("periods") or []):
            period_name_raw: str = (period.get("name") or "").strip()
            if not period_name_raw:
                continue
            period_key = PERIOD_NAME_MAP.get(period_name_raw, period_name_raw.lower())

            stations_out: Dict[str, List[str]] = {}
            for st in (period.get("stations") or []):
                station_name = (st.get("name") or "").strip()
                if not station_name:
                    continue
                items = _extract_items(st)
                if items:  # only add stations with items
                    stations_out[station_name] = items

            if stations_out:  # only add periods with stations
                hall_periods[period_key] = stations_out

        if hall_periods:  # only add halls with periods
            result[hall_name] = hall_periods

    return result

def normalize_meals(barnard_dict: Dict[str, Dict[str, Dict[str, List[str]]]]
                    ) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    """
    Hook for later tweaks (e.g., merging lunch & dinner → 'lunch & dinner' if you want).
    Currently pass-through because Barnard exposes separate periods already.
    """
    return barnard_dict

def bscrape() -> Dict[str, Dict[str, Dict[str, List[str]]]]:
    """Public entry point imported by scrape.py"""
    payload = _fetch_barnard_raw()
    return parse_barnard_to_columbia_shape(payload)

if __name__ == "__main__":
    data = _fetch_barnard_raw()
    parsed = parse_barnard_to_columbia_shape(data)
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
