from flask import Flask, render_template, g
from datetime import datetime
import os
import json
import boto3
import pytz

from dining_config import (
    is_hall_open, get_station_mapping, get_hardcoded_menu, 
    get_all_hall_names, get_hours_for_meal
)
# Break schedule overrides - uncomment the one you need:
from time_functions import winter_hours  # Current: winter break
# from time_functions import nsop_hours  # For orientation
# from time_functions import all_closed  # For summer

app = Flask(__name__) #sets up a flask application
app.secret_key = os.environ.get('SECRET_KEY','fallback-secret-key') 

ny_tz = pytz.timezone('America/New_York')

dining_halls = get_all_hall_names()

# Gets dining data from AWS S3, with local file fallback for development
def get_dining_data():
  bucket_name = 'lion-dine-data'
  object_name = 'dining_data.json'
  s3_client = boto3.client('s3')
  #boto3 automatically looks for credentials stored locally
  try:
    response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    content = response['Body'].read().decode('utf-8')
    data = json.loads(content)
    return data
  except Exception as e:
    print(f"Error fetching data from AWS S3: {e}")
    return {}

def open_at_meal(now, meal):
    halls = get_dining_data()
    filtered_halls = {}
    weekday = now.weekday()
    
    # ==========================================================================
    # SCHEDULE MODE: Toggle between regular semester and break schedules
    # ==========================================================================
    # For regular semester, use get_hours_for_meal (pulls from dining_config.py)
    # For breaks, use the override function (winter_hours, nsop_hours, etc.)
    
    USE_BREAK_SCHEDULE = True  # Set to False for regular semester
    
    if USE_BREAK_SCHEDULE:
        # Break mode: use override hours (same hours dict for all meals)
        hours_for_meal = winter_hours(weekday, now)
    else:
        # Regular semester: pull hours from dining_config.py
        hours_for_meal = get_hours_for_meal(weekday, meal)
    
    # Initialize all halls and determine open/closed status
    for hall_name in dining_halls:
        hall_hours = hours_for_meal.get(hall_name, "Hours not available")
        
        # Determine if hall is open based on schedule mode
        if USE_BREAK_SCHEDULE:
            # During breaks: open if hours don't say "Closed"
            is_open = not hall_hours.startswith("Closed")
        else:
            # Regular semester: use the schedule from dining_config.py
            is_open = is_hall_open(hall_name, weekday, meal)
        
        filtered_halls[hall_name] = {
            'status': "Open" if is_open else f'Closed for {meal}',
            'hours': hall_hours,
            'stations': {},
        }
    
    # Process stations for open halls
    for hall_name, stations in halls.items():
        if hall_name not in filtered_halls:
            continue
            
        if filtered_halls[hall_name]["status"].startswith("Closed"):
            continue
            
        if stations is None:
            filtered_halls[hall_name]["stations"] = "Missing data"
            continue
        
        # Get station mapping for this hall and meal
        station_types = get_station_mapping(hall_name, meal)
        filtered_stations = {}
        
        # Check if this hall uses hardcoded menus
        hardcoded_menu = get_hardcoded_menu(hall_name, meal)
        if hardcoded_menu:
            filtered_stations = hardcoded_menu
        else:
            # Process scraped data based on station mapping
            for station_type in station_types:
                if station_type in stations:
                    for station_name, items in stations[station_type].items():
                        if station_name in filtered_stations:
                            # Merge items if station already exists
                            filtered_stations[station_name].extend(items)
                        else:
                            filtered_stations[station_name] = items
        
        # Set stations data
        if filtered_stations:
            filtered_halls[hall_name]["stations"] = filtered_stations
        else:
            filtered_halls[hall_name]["stations"] = "Missing data"
    
    return filtered_halls

#mapping URLs to functions that display the HTML we want for that URL
def get_current_time():
  #Helper to fetch or reuse the current time for this request.
  if not hasattr(g, 'now'):
      g.now = datetime.now(ny_tz)
  return g.now

@app.before_request
def set_current_time():
  #Set the current time once per request.
  g.now = datetime.now(ny_tz)


@app.route('/') 
def index():
  now = get_current_time()
  if now.hour >= 4 and now.hour < 11:
    return breakfast()
  elif now.hour >= 11 and now.hour < 16:
    return lunch()
  elif now.hour >= 16 and now.hour <= 21:
    return dinner()
  else:
    return latenight()
  
@app.route('/breakfast')
def breakfast():
  now = get_current_time()
  filtered_halls = open_at_meal(now, "breakfast")
  return render_template('index.html', halls=filtered_halls, meal="breakfast", current_time=now)

@app.route('/lunch')
def lunch():
  now = get_current_time()
  filtered_halls = open_at_meal(now, "lunch")
  return render_template('index.html', halls=filtered_halls, meal="lunch", current_time=now)

@app.route('/dinner')
def dinner():
  now = get_current_time()
  filtered_halls = open_at_meal(now, "dinner")
  return render_template('index.html', halls=filtered_halls, meal="dinner", current_time=now)

@app.route('/latenight')
def latenight():
  now = get_current_time()
  filtered_halls = open_at_meal(now, "latenight")
  return render_template('index.html', halls=filtered_halls, meal="latenight", current_time=now)

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5000, debug=True)