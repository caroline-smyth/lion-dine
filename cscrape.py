import cloudscraper
from datetime import datetime
import json, boto3

scraper = cloudscraper.create_scraper()

date = datetime.now().date().isoformat()
base = "https://dining.columbia.edu/cu_dining/rest"
dining_hall_data = {}

loc_resp   = scraper.get(f"{base}/occuspace_locations").json()
locations  = [l for l in loc_resp["data"] if l["isActive"]]

columbia = {}