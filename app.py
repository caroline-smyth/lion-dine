from flask import Flask, render_template
from datetime import datetime, time 
import time as time_module
import random
import os
import requests
import json
import boto3
from time_functions import john_jay_open, jjs_open, ferris_open, fac_house_open, mikes_open, dons_open, grace_dodge_open, fac_shack_open, hewitt_open, diana_open, hours_dict, breakfast_hours, lunch_hours, dinner_hours, latenight_hours
import pytz
from flask import make_response, g, render_template

app = Flask(__name__) #sets up a flask application 

ny_tz = pytz.timezone('America/New_York')

dining_halls = [
  "John Jay",
  "JJ's",
  "Ferris",
  "Faculty House",
  "Chef Mike's",
  "Chef Don's",
  "Grace Dodge",
  "Fac Shack", 
  "Hewitt Dining", 
  "Diana Center Cafe",
  "Hewitt Kosher"
]

#gets dining data from dropbox json file
def get_dining_data():
  bucket_name = 'liondine-data'
  object_name = 'dining_data.json'
  s3_client = boto3.client('s3')

  try:
    response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
    content = response['Body'].read().decode('utf-8')
    data = json.loads(content)
    return data
  except Exception as e:
    print(f"Error fetching data from AWS S3: {e}")
    return {}


#takes the dictionary of all food items and filters it to only include
#stations that are currently open
def current_open_stations(now):
  halls = get_dining_data()
  print(halls)
  filtered_halls = {} #to be filled

  #if a dining hall is closed, give it value "Closed" instead of a list of food

  closed_check = [
    ("John Jay", john_jay_open),
    ("JJ's", jjs_open),
    ("Ferris", ferris_open),
    ("Faculty House", fac_house_open),
    ("Chef Mike's", mikes_open),
    ("Chef Don's", dons_open),
    ("Grace Dodge", grace_dodge_open),
    ("Fac Shack", fac_shack_open),
    ("Hewitt Dining", hewitt_open),
    ("Diana Center Cafe", diana_open)
    ]
  
  hours = hours_dict(now.weekday())

  for hall_name, is_open_func in closed_check:
    # Initialize with hours for all halls
    filtered_halls[hall_name] = {
        "status": "Open" if is_open_func(now) else "Closed",
        "hours": hours.get(hall_name, "Hours not available"),
        "stations": {},
    }

  #for each dining hall, skipping the closed ones, find each station that's currently open and add it to the filtered dictionary
  
  for hall_name, stations in halls.items():
    if hall_name in filtered_halls and filtered_halls[hall_name]["status"].startswith("Closed"):
      continue
    if stations is None:
      filtered_halls[hall_name]["stations"] = "Missing data"
      continue
  
    filtered_stations = {}
    
    #this code will replace the below code once we have all scraped data.
    #here, we hard-code the times of each station of each dining hall.
    if hall_name == "John Jay":
      if now.weekday() == 6:
        if 10 <= now.hour and now.hour < 11 or (now.hour == 9 and now.minute >= 30):
          for station, items in stations.get('brunch',{}).items():
            filtered_stations[station] = items
        if 11 <= now.hour and now.hour < 14 or (now.hour == 14 and now.minute < 30):
          for station, items in stations.get('lunch',{}).items():
            filtered_stations[station] = items
        for station, items in stations.get('lunch & dinner',{}).items():
          filtered_stations[station] = items
        if 17 <= now.hour and now.hour < 21:
          for station, items in stations.get('dinner',{}).items():
            filtered_stations[station] = items
          for station, items in stations.get('lunch & dinner',{}).items():
            filtered_stations[station] = items
      if now.weekday() in [0, 1, 2, 3]:
        if 10 <= now.hour and now.hour < 11 or (now.hour == 9 and now.minute >= 30):
          for station, items in stations.get('breakfast',{}).items():
            filtered_stations[station] = items
      
        if 11 <= now.hour and now.hour < 14 or (now.hour == 14 and now.minute < 30):
          for station, items in stations.get('lunch',{}).items():
            filtered_stations[station] = items
          for station, items in stations.get('lunch & dinner',{}).items():
            filtered_stations[station] = items
        if 17 <= now.hour and now.hour < 21:
          for station, items in stations.get('dinner',{}).items():
            filtered_stations[station] = items
          for station, items in stations.get('lunch & dinner',{}).items():
            filtered_stations[station] = items
        #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing Data"
    
    if hall_name == "JJ's":
      #filter for only open stations
      #filtered_stations["all hours"] = "12 pm - 10 am"
      if now.hour >= 12 or now.hour < 4:
        for station, items in stations.get('lunch & dinner',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:
            filtered_stations[station] = items
      if now.hour > 22 or now.hour < 4:
        for station, items in stations.get('late night',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:          
            filtered_stations[station] = items
      if now.hour >= 4 and now.hour < 10:
        for station, items in stations.get('breakfast',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:          
            filtered_stations[station] = items
      #return data to the filtered dictionary

      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing Data"

    if hall_name == "Ferris":
      if now.weekday() in [0,1,2,3,4]:
        #filtered_stations["all hours"] = "7:30 am - 8 pm"
        if now.hour > 7 and now.hour < 11 or (now.hour == 7 and now.minute >= 30):
          for station, items in stations.get('breakfast',{}).items():
            filtered_stations[station] = items
        if now.hour >= 11 and now.hour < 16:
          for station, items in stations.get('lunch',{}).items():
            filtered_stations[station] = items
        if now.hour >= 17 and now.hour < 20:
          for station, items in stations.get('dinner',{}).items():
            filtered_stations[station] = items
        if now.hour >= 11 and now.hour < 20:
          for station, items in stations.get('lunch & dinner',{}).items():
            filtered_stations[station] = items
      if now.weekday() == 5:
        if now.hour <= 11 and (now.hour > 9):
          for station, items in stations.get('breakfast',{}).items():
            filtered_stations[station] = items
        if now.hour >= 11 and now.hour < 2:
          for station, items in stations.get('lunch',{}).items():
            filtered_stations[station] = items
          for station, items in stations.get('lunch & dinner',{}).items():
            filtered_stations[station] = items
        if now.hour >= 17 and now.hour < 20:
          for station, items in stations.get('dinner',{}).items():
            filtered_stations[station] = items
          for station, items in stations.get('lunch & dinner',{}).items():
            filtered_stations[station] = items
      if now.weekday() == 6:
        #filtered_stations["all hours"] = "10 am - 2 pm, 5 pm - 8 pm"
        if (now.hour == 7 and now.minute >= 30) or (now.hour >= 8 and now.hour < 11):
          for station, items in stations.get('breakfast', {}).items():
            filtered_stations[station] = items

        if now.hour >= 11 and now.hour < 14:
          for station, items in stations.get('lunch',{}).items():
            filtered_stations[station] = items
          for station, items in stations.get('lunch & dinner',{}).items():
            filtered_stations[station] = items
        if now.hour >= 17 and now.hour < 20:
          for station, items in stations.get('dinner',{}).items():
            filtered_stations[station] = items
          for station, items in stations.get('lunch & dinner',{}).items():
            filtered_stations[station] = items
    #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
        #filtered_halls[hall_name]["stations"]["Missing Data"] = ""
      else:
        filtered_halls[hall_name]["stations"] = "Missing Data"

    if hall_name == "Faculty House":
      #filter for only open stations
      #filtered_stations["all hours"] = "11 am - 2:30 pm"
      for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data"

    if hall_name == "Chef Mike's":
      #filter for only open stations
      #filtered_stations["all hours"] = "10:30 am - 10 pm"
      for station, items in stations.get('lunch & dinner',{}).items():
        filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
        #filtered_halls[hall_name]["stations"]["Missing Data"] = ""
      else:
        filtered_halls[hall_name]["stations"] = "Missing Data"    

    if hall_name == "Chef Don's":
      #filtered_stations["all hours"] = "8 am - 6 pm"
      if now.hour >= 8 and now.hour < 11:
        filtered_stations["Breakfast"] = ["Bacon egg and cheese bagel", "Ham egg and cheese bagel", "Vegan breakfast bagel", "Cup of oatmeal", "Piece of fruit","Danish pastry","Small coffee or tea"]
      if now.hour >= 11 and now.hour < 18:
        filtered_stations["Lunch/Dinner Service"] = ["Build your own pizza", "Toasted Cuban sandwich", "Piece of fruit", "Milkshake or Freestyle machine beverage", "Dessert"]
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
        #filtered_halls[hall_name]["stations"]["Missing Data"] = ""
      else:
        filtered_halls[hall_name]["stations"] = "Missing Data"

    if hall_name == "Grace Dodge":
      #filter for only open stations
      #filtered_stations["all hours"] = "11 am - 7 pm"
      for station, items in stations.get('lunch & dinner',{}).items():
        filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
        #filtered_halls[hall_name]["stations"]["Missing Data"] = ""
      else:
        filtered_halls[hall_name]["stations"] = "Missing Data"
    
    if hall_name == "Fac Shack":
      if now.weekday() in [0,1,2,3] and now.hour >= 11 and now.hour < 14:
        #filtered_stations["all hours"] = "11 am - 2 pm"
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      if now.weekday() in [3,4,5] and now.hour >= 19 and now.hour < 23:
        #filtered_stations["all hours"] = "7 pm - 11 pm"
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
        #filtered_halls[hall_name]["stations"]["Missing Data"] = ""
      else:
        filtered_halls[hall_name]["stations"] = "Missing Data"

    if hall_name == "Hewitt Dining":
      if (now.weekday() in [0, 1, 2, 3, 4] and ((now.hour > 7 and now.hour < 10) or now.hour == 7 and now.minute > 30)) or (now.weekday() in [5, 6] and ((now.hour > 10 and now.hour < 12) or (now.hour == 10 and now.minute > 30))):
        for station, items in stations.get('breakfast',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('every day',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('brunch',{}).items():
          filtered_stations[station] = items
      if (now.weekday() in [0, 1, 2, 3, 4] and ((now.hour >= 11 and now.hour < 14) or (now.hour == 14 and now.minute < 30))) or (now.weekday() in [5, 6] and (now.hour > 12 and now.hour < 15)):
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('every day',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('brunch',{}).items():
          filtered_stations[station] = items
      if (now.hour > 16 and now.hour < 30) or (now.hour == 16 and now.minute > 30):
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('every day',{}).items():
          filtered_stations[station] = items
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing Data"
      
    if hall_name == "Diana Center Cafe":
      if (now.weekday() in [0, 1, 2, 3] and ((now.hour >= 9 and now.hour < 11) or (now.hour == 11 and now.minute < 30))) or (now.weekday() == 4 and (now.hour >= 9 and now.hour < 12)):
        for station, items in stations.get('breakfast',{}).items():
          filtered_stations[station] = items  
      if (now.weekday() in [0, 1, 2, 3] and ((now.hour > 11 and now.hour < 17) or (now.hour == 11 and now.minute > 30))) or (now.weekday() == 4 and (now.hour >= 12 and now.hour < 15) or (now.weekday() == 6 and (now.hour >= 12 and now.hour < 17))):
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items   
      if now.weekday() in [0, 1, 2, 3, 6] and ((now.hour >= 17 and now.hour < 20)):
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items       
      if now.weekday() in [0, 1, 2, 3] and (now.hour >= 20):
        for station, items in stations.get('late night',{}).items():
          filtered_stations[station] = items

      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing Data"
  
  return filtered_halls

#takes the dictionary of all food items and filters it to only include
#stations that are open at the given meal

def open_at_meal(now, meal):
  halls = get_dining_data()
  print("Dining hall names: ", halls.keys())
  print(halls)
  filtered_halls = {} #to be filled

  for hall_name in dining_halls:
    filtered_halls[hall_name] = {
      'status': 'Unknown',
      'hours': 'Hours not available',
      'stations': {},
    }

  # CHECKS FOR CLOSED
  
  b_hours = breakfast_hours(now.weekday(), now)
  l_hours = lunch_hours(now.weekday(), now)
  d_hours = dinner_hours(now.weekday(), now)
  ln_hours = latenight_hours(now.weekday(), now)

  #filtered_halls[hall_name]["status"] = "Open" if meal in meal_list else f"Closed for {meal}"

  filtered_halls["John Jay"]["status"] = "Open" if now.weekday() in [6,0,1,2,3] else f"Closed for {meal}"
  filtered_halls["JJ's"]["status"] = "Open" #FALL BREAK
  filtered_halls["Ferris"]["status"] = "Open"
  filtered_halls["Hewitt Dining"]["status"] = "Open"
  if (now.weekday() == 5 and meal in ["breakfast", "lunch", "dinner", "latenight"]):
    filtered_halls["Hewitt Kosher"]["status"] = f"Closed for {meal}"
  elif (now.weekday() == 4 and meal == "dinner"):
    filtered_halls["Hewitt Kosher"]["status"] = f"Closed for {meal}"
  else:
    filtered_halls["Hewitt Kosher"]["status"] = "Open"
  if now.weekday() in [0,1,2] and meal == "lunch":
    filtered_halls["Faculty House"]["status"] = "Open"
  else:
    filtered_halls["Faculty House"]["status"] = f"Closed for {meal}"
  if now.weekday() in [0,1,2,3,4] and meal in ["lunch","dinner"]:
    filtered_halls["Chef Mike's"]["status"] = "Open"
  else:
    filtered_halls["Chef Mike's"]["status"] = f"Closed for {meal}"
  if now.weekday() in [0,1,2,3,4]:
    filtered_halls["Chef Don's"]["status"] = "Open"
  else:
    filtered_halls["Chef Don's"]["status"] = f"Closed for {meal}"
  if now.weekday() in [0,1,2,3] and meal in ["lunch","dinner"]:
    filtered_halls["Grace Dodge"]["status"] = "Open"
  else:
    filtered_halls["Grace Dodge"]["status"] = f"Closed for {meal}"
  if (now.weekday() in [0,1,2,3] and meal == "lunch" or
      now.weekday() in [3,4,5] and (meal == "dinner" or meal == "latenight")):
    filtered_halls["Fac Shack"]["status"] = "Open"
  else:
    filtered_halls["Fac Shack"]["status"] = f"Closed for {meal}"
  if (now.weekday() in [0,1,2,3] or (now.weekday() == 4 and meal in ["breakfast", "lunch"]) or 
      now.weekday() == 6 and meal in ["lunch","dinner"]):
    filtered_halls["Diana Center Cafe"]["status"] = "Open"
  elif now.weekday() in [0, 1, 2, 3] and meal == "latenight":
    filtered_halls["Diana Center Cafe"]["status"] = "Open"
  else:
    filtered_halls["Diana Center Cafe"]["status"] = f"Closed for {meal}"
  if meal == "latenight":
    filtered_halls["Ferris"]["status"] = filtered_halls["John Jay"]["status"] = filtered_halls["Faculty House"]["status"] = filtered_halls["Chef Mike's"]["status"] = filtered_halls["Chef Don's"]["status"] = filtered_halls["Hewitt Dining"]["status"] = filtered_halls["Hewitt Kosher"]["status"] = f"Closed for {meal}"

  # FALL BREAK 
  """
  if now.month == 11 and now.day in [3, 4, 5]:
    filtered_halls["Chef Don's"]["status"] = filtered_halls["Chef Mike's"]["status"] = filtered_halls["Ferris"]["status"] = filtered_halls["Faculty House"]["status"] = filtered_halls["Fac Shack"]["status"] = filtered_halls["Grace Dodge"]["status"] = filtered_halls["Diana Center Cafe"]["status"] = "Closed today"
    if meal in ["breakfast", "lunch", "dinner"]:
      filtered_halls["JJ's"]["status"] = "Open"
    else:
      filtered_halls["JJ's"]["status"] = "Closed for late night"
    """
  
  if now.month == 12 or now.month == 1:
    filtered_halls["Chef Don's"]["status"] = filtered_halls["Chef Mike's"]["status"] = filtered_halls["Ferris"]["status"] = filtered_halls["Faculty House"]["status"] = filtered_halls["Fac Shack"]["status"] = filtered_halls["Grace Dodge"]["status"] = filtered_halls["Diana Center Cafe"]["status"] = filtered_halls["John Jay"]["status"] = filtered_halls["JJ's"]["status"] = filtered_halls["Diana Center Cafe"]["status"] = filtered_halls["Hewitt Dining"]["status"] = "Closed today"
  
  if now.month == 12 and now.day in [25, 26, 27, 28, 29, 30, 31] or (now.month == 1 and now.day in [1, 2, 3, 4]):
    filtered_halls["Fac Shack"]["status"] = "Open"
    if meal == "latenight":
      filtered_halls["Fac Shack"]["status"] = "Closed for late night"
  if now.month == 1 and (now.day > 4 and now.day <= 17):
    if meal in ["breakfast", "lunch", "dinner"]:
      filtered_halls["JJ's"]["status"] = "Open"
    else:
      filtered_halls["JJ's"]["status"] = "Closed for late night"
  if now.month == 1 and now.day in [18,19,20]:
    filtered_halls["Ferris"]["status"] = "Open"
    if meal == "latenight":
      filtered_halls["Ferris"]["status"] = "Closed for late night"

  for hall_name in halls.keys():
    if meal == "breakfast":
      filtered_halls[hall_name]["hours"] = b_hours.get(hall_name, "Hours not available")
    elif meal == "lunch":
      filtered_halls[hall_name]["hours"] = l_hours.get(hall_name, "Hours not available")
    elif meal == "dinner":
      filtered_halls[hall_name]["hours"] = d_hours.get(hall_name, "Hours not available")
    elif meal == "latenight":
      filtered_halls[hall_name]["hours"] = ln_hours.get(hall_name, "Hours not available")

  #for each dining hall, skipping the closed ones, find each
  #station that's currently open and add it to the filtered dictionary
  for hall_name, stations in halls.items():
    if hall_name in filtered_halls and filtered_halls[hall_name]["status"].startswith("Closed"):
      continue
    filtered_stations = {}
    
    if stations is None:
      filtered_halls[hall_name]["stations"] = "Missing data"
      continue

    #this code will replace the below code once we have all scraped data.
    #here, we hard-code the times of each station of each dining hall.
    if hall_name == "John Jay" or hall_name == "Ferris":
      #filter for only open stations
      if meal == 'breakfast':
        for station, items in stations.get('breakfast',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('brunch',{}).items():
          filtered_stations[station] = items         
      if meal == 'lunch':
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('lunch & dinner',{}).items():
          filtered_stations[station] = items
      if meal == 'dinner':
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('lunch & dinner',{}).items():
          filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data"  
    if hall_name == "JJ's":
      #filter for only open stations
      if meal == 'breakfast':
        for station, items in stations.get('breakfast',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:
            filtered_stations[station] = items
        for station, items in stations.get('daily',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:
            filtered_stations[station] = items 
      if meal == 'lunch':
        for station, items in stations.get('lunch & dinner',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:          
            filtered_stations[station] = items
        for station, items in stations.get('daily',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:          
            filtered_stations[station] = items
      if meal == 'dinner':
        for station, items in stations.get('daily',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:          
            filtered_stations[station] = items
        for station, items in stations.get('lunch & dinner',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:
            filtered_stations[station] = items
        for station, items in stations.get('late night',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:          
            filtered_stations[station] = items
      if meal == 'latenight':
        for station, items in stations.get('lunch & dinner',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:
            filtered_stations[station] = items
        for station, items in stations.get('late night',{}).items():
          if station in filtered_stations:
            filtered_stations[station].extend(items)
          else:          
            filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data"
    if hall_name == "Faculty House":
      #filter for only open stations
      if meal == 'lunch':
        for station, items in stations.get('lunch',{}).items():
            filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data" 
    if hall_name == "Chef Mike's":
      #filter for only open stations
      if meal == 'lunch' or meal == 'dinner':
        for station, items in stations.get('lunch & dinner',{}).items():
          filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data"      
    if hall_name == "Chef Don's":
      if meal == 'breakfast':
        filtered_stations["Sandwiches"] = ["Bacon egg and cheese bagel", "Ham egg and cheese bagel", "Vegan breakfast bagel"]
        filtered_stations["Sides"] = ["Cup of oatmeal", "Piece of fruit","Danish pastry","Small coffee or tea"]
      if meal == 'lunch' or meal == 'dinner':
        filtered_stations["Entree"] = ["Build your own pizza", "Toasted Cuban sandwich"]
        filtered_stations["Sides"] = ["Piece of fruit", "Soup","Milkshake","Freestyle machine beverage", "Dessert"]
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data"    
    if hall_name == "Grace Dodge":
      #filter for only open stations
      if meal == 'lunch' or meal == 'dinner':
        filtered_stations["Salad Base"] = ["Spinach", "Spring Green Mix", "Romaine"]
        filtered_stations["Grains"] = ["Brown Rice", "White Rice"]
        filtered_stations["Cold Toppings & Protein"] = ["Bell Peppers", "Black Beans", "Chickpeas", "Corn", "Cucumbers", "Red Onion", "Shredded Carrots", "Tofu", "Tomatoes"]
        filtered_stations["Hot Toppings & Protein"] = ["Rotates Daily"]
        filtered_stations["Ramen Broth"] = ["Tonkatsu", "Shiro Miso Kombu Dashi"]
        filtered_stations["Noodles"] = ["Yakisoba", "Vermicelli"]
        filtered_stations["Toppings"] = ["Bok Choy","Bean Sprouts","Cilantro","Corn","Kimchi","Marinated Egg", "Scallions","Sauteed Shiitake Mushrooms","Shredded Carrots","Tofu"]
        filtered_stations["Protein"] = ["Rotates Daily"]
        filtered_stations["Sides"] = ["Fruit","Beverage","Dessert"]
        for station, items in stations.get('lunch & dinner',{}).items():
          filtered_stations[station] = items
        
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data"
    if hall_name == "Fac Shack":
      if meal == 'lunch':
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      if meal == 'dinner' or meal == 'latenight':
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data"
    if hall_name == "Hewitt Dining":
      if meal == 'breakfast':
        for station, items in stations.get('breakfast',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('brunch',{}).items():
          filtered_stations[station] = items
      elif meal == 'lunch':
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('brunch',{}).items():
          filtered_stations[station] = items
      elif meal == 'dinner':
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
      for station, items in stations.get('every day',{}).items():
        filtered_stations[station] = items
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data"
    if hall_name == "Hewitt Kosher":
      if meal == 'breakfast':
        for station, items in stations.get('breakfast',{}).items():
          filtered_stations[station] = items
      if meal == 'lunch':
        for station, items in stations.get('brunch',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      if meal == 'dinner':
        for station, items in stations.get('brunch',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
    if hall_name == "Diana Center Cafe":
      if meal == 'breakfast':
        for station, items in stations.get('breakfast',{}).items():
          filtered_stations[station] = items
      if meal == 'lunch':
        for station, items in stations.get('brunch',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      if meal == 'dinner':
        for station, items in stations.get('brunch',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
      if meal == 'latenight':
        for station, items in stations.get('late night',{}).items():
          filtered_stations[station] = items
      if filtered_stations:
        filtered_halls[hall_name]["stations"] = filtered_stations
      else:
        filtered_halls[hall_name]["stations"] = "Missing data"
  
  return filtered_halls

#mapping URLs to functions that display the HTML we want for that URL
def get_current_time():
  """Helper to fetch or reuse the current time for this request."""
  if not hasattr(g, 'now'):
      g.now = datetime.now(ny_tz)
  return g.now

@app.before_request
def set_current_time():
  """Set the current time once per request."""
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
   app.run(host='0.0.0.0',port=5000)