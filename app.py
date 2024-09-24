from flask import Flask, render_template
from datetime import datetime, time 
import time as time_module
import random
import os
import requests
import json

app = Flask(__name__) #sets up a flask application

#gets dining data from dropbox json file
def get_dining_data():
  try:
    url = 'https://www.dropbox.com/scl/fi/xw1hdarlxp669mrqj3b9q/dining_data.json?rlkey=canzljc67mwx9lahdy0ps1bvl&st=y00ueu6e&dl=1'
    response = requests.get(url)
    data = response.json()
    return data
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from Dropbox: {e}")
    return {}
  except json.JSONDecodeError as e:
    print(f"Error decoding JSON data: {e}")
    return {}


#takes the dictionary of all food items and filters it to only include
#stations that are currently open
def current_open_stations():
  now = datetime.now()
  halls = get_dining_data()
  print(halls)
  filtered_halls = {} #to be filled

  #if a dining hall is closed, give it value "Closed" instead
  #of a list of food

  # john jay
  if now.weekday() in [4,5] or now.hour < 9 or now.hour >= 21 or (now.hour == 9 and now.minute < 30):
    filtered_halls["John Jay"] = "Closed"
  #jjs
  if now.hour in [10,11]:
    filtered_halls["JJ's"] = "Closed"
  #ferris
  if ((now.weekday() in [0,1,2,3,4] and (now.hour < 7 or now.hour >= 20 or (now.hour == 7 and now.minute < 30))) or
      (now.weekday() == 5 and (now.hour < 9 or now.hour >= 20)) or
      (now.weekday() == 6 and (now.hour < 10 or now.hour >= 20 or now.hour in [15,16]))):
    filtered_halls["Ferris"] = "Closed"
  #fac house
  if now.weekday() > 2 or now.hour < 11 or now.hour > 14 or (now.hour == 14 and now.minute > 30):
    filtered_halls["Faculty House"] = "Closed"
  #mikes
  if now.weekday() in [5,6] or now.hour < 10 or now.hour >= 22 or (now.hour == 10 and now.minute < 30):
    filtered_halls["Chef Mike's"] = "Closed"
  #dons
  if now.weekday() in [5,6] or now.hour < 8 or now.hour >= 18:
    filtered_halls["Chef Don's"] = "Closed"
  #grace dodge
  if now.weekday() in [4,5,6] or now.hour < 11 or now.hour >= 19:
    filtered_halls["Grace Dodge"] = "Closed"
  #fac shack
  if (now.weekday() == 6) or (now.weekday() in [0,1,2] and (now.hour < 11 or now.hour >= 14) or
      (now.weekday() in [4,5] and (now.hour < 19 or now.hour >= 23)) or
      (now.weekday() == 3 and (now.hour < 11 or now.hour >= 23 or now.hour in [14,15,16,17,18]))):
    filtered_halls["Fac Shack"] = "Closed"
  #hewitt
  if ((now.weekday() in [0,1,2,3,4] and 
       now.hour < 7 or (now.hour == 7 and now.minute < 30) or now.hour == 10 or
       (now.hour == 14 and now.minute > 30) or now.hour == 15 or 
       (now.hour == 16 and now.minute < 30) or now.hour >= 20) or
      (now.weekday() in [5,6] and 
       now.hour < 10 or (now.hour == 10 and now.minute < 30) or now.hour == 15 or
       (now.hour == 16 and now.minute < 30) or now.hour >= 20)):
    filtered_halls["Hewitt"] = "Closed"
  #diana
  if ((now.weekday() in [0,1,2,3] and (now.hour < 9 or now.hour in [15,16])) or 
      (now.weekday() == 4 and (now.hour < 9 or now.hour >= 15)) or
      (now.weekday() == 5) or 
      (now.weekday() == 6 and (now.hour < 12 or now.hour > 20))):
    filtered_halls["Diana"] = "Closed"
  

  #dummy_halls = dummy_food() #for testing

  #for each dining hall, skipping the closed ones, find each
  #station that's currently open and add it to the filtered dictionary
  
  for hall_name, stations in halls.items():
  #for hall_name, stations in dummy_halls.items():
    if hall_name in filtered_halls and filtered_halls[hall_name] == "Closed":
      continue
    filtered_stations = {}
    
    #this code will replace the below code once we have all scraped data.
    #here, we hard-code the times of each station of each dining hall.
    if hall_name == "John Jay":
      #filter for only open stations
      filtered_stations["all hours"] = "9:30 am - 9 pm"
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
      if len(filtered_stations) == 1:
        filtered_halls[hall_name] = filtered_stations
        filtered_halls[hall_name]["Missing Data"] = ""
      else:
        filtered_halls[hall_name] = filtered_stations 
    
    if hall_name == "JJ's":
      #filter for only open stations
      filtered_stations["all hours"] = "12 pm - 10 am"
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
      if len(filtered_stations) == 1:
        filtered_halls[hall_name] = filtered_stations
        filtered_halls[hall_name]["Missing Data"] = ""
      else:
        filtered_halls[hall_name] = filtered_stations 

    if hall_name == "Ferris":
      if now.weekday() in [0,1,2,3,4]:
        filtered_stations["all hours"] = "7:30 am - 8 pm"
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
        filtered_stations["all hours"] = "9 am - 8 pm"
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
        filtered_stations["all hours"] = "10 am - 2 pm, 5 pm - 8 pm"
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
      if len(filtered_stations) == 1:
        filtered_halls[hall_name] = filtered_stations
        filtered_halls[hall_name]["Missing Data"] = ""
      else:
        filtered_halls[hall_name] = filtered_stations

    if hall_name == "Faculty House":
      #filter for only open stations
      filtered_stations["all hours"] = "11 am - 2:30 pm"
      for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"

    if hall_name == "Chef Mike's":
      #filter for only open stations
      filtered_stations["all hours"] = "10:30 am - 10 pm"
      for station, items in stations.get('lunch & dinner',{}).items():
        filtered_stations[station] = items
      #return data to the filtered dictionary
      if len(filtered_stations) == 1:
        filtered_halls[hall_name] = filtered_stations
        filtered_halls[hall_name]["Missing Data"] = ""
      else:
        filtered_halls[hall_name] = filtered_stations     

    if hall_name == "Chef Don's":
      filtered_stations["all hours"] = "8 am - 6 pm"
      if now.hour >= 8 and now.hour < 11:
        filtered_stations["Breakfast"] = ["Breakfast Sandwich"]
      if now.hour >= 11 and now.hour < 18:
        filtered_stations["Pizza"] = ["Build your own"]
      if len(filtered_stations) == 1:
        filtered_halls[hall_name] = filtered_stations
        filtered_halls[hall_name]["Missing Data"] = ""
      else:
        filtered_halls[hall_name] = filtered_stations 

    if hall_name == "Grace Dodge":
      #filter for only open stations
      filtered_stations["all hours"] = "11 am - 7 pm"
      for station, items in stations.get('lunch & dinner',{}).items():
        filtered_stations[station] = items
      #return data to the filtered dictionary
      if len(filtered_stations) == 1:
        filtered_halls[hall_name] = filtered_stations
        filtered_halls[hall_name]["Missing Data"] = ""
      else:
        filtered_halls[hall_name] = filtered_stations 
    
    if hall_name == "Fac Shack":
      if now.weekday() in [0,1,2,3] and now.hour >= 11 and now.hour < 14:
        filtered_stations["all hours"] = "11 am - 2 pm"
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      if now.weekday() in [3,4,5] and now.hour >= 19 and now.hour < 23:
        filtered_stations["all hours"] = "7 pm - 11 pm"
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
      if len(filtered_stations) == 1:
        filtered_halls[hall_name] = filtered_stations
        filtered_halls[hall_name]["Missing Data"] = ""
      else:
        filtered_halls[hall_name] = filtered_stations 

    if hall_name == "Hewitt":
      if len(filtered_stations) == 1:
        filtered_halls[hall_name] = filtered_stations
        filtered_halls[hall_name]["Missing Data"] = ""
      else:
        filtered_halls[hall_name] = filtered_stations 
    if hall_name == "Diana":
      if len(filtered_stations) == 1:
        filtered_halls[hall_name] = filtered_stations
        filtered_halls[hall_name]["Missing Data"] = ""
      else:
        filtered_halls[hall_name] = filtered_stations 
    

  
    #test code, using time data that is built into the dictionary.
    #our real dictionary won't have this time data.
    '''
    for station_name, station_info in stations.items():
      open_time, close_time = station_info["hours"]
      if open_time <= now.time() <= close_time:
        filtered_stations[station_name] = station_info["items"]
    if filtered_stations:
      filtered_halls[hall_name] = filtered_stations
    else:
      filtered_halls[hall_name] = "Missing Data"
    '''
  
  return filtered_halls

#takes the dictionary of all food items and filters it to only include
#stations that are open at the given meal
def open_at_meal(meal):
  now = datetime.now()
  halls = get_dining_data()
  print(halls)
  filtered_halls = {} #to be filled


  # CHECKS FOR CLOSED

  #ferris, JJs, hewitt are open every meal every day
  # john jay
  if now.weekday() in [4,5]:
    filtered_halls["John Jay"] = f"Closed for {meal}"
  # fac house
  if now.weekday() > 2 or meal == "breakfast" or meal == "dinner":
    filtered_halls["Faculty House"] = f"Closed for {meal}"
  #mikes
  if now.weekday() in [5,6] or meal == "breakfast":
    filtered_halls["Chef Mike's"] = f"Closed for {meal}"
  #don's
  if now.weekday() in [5,6]:
    filtered_halls["Chef Don's"] = f"Closed for {meal}"
  #grace dodge
  if now.weekday() in [4,5,6] or meal == "breakfast":
    filtered_halls["Grace Dodge"] = f"Closed for {meal}"
  #fac shack
  if not ((now.weekday() in [0,1,2,3] and meal == "lunch") or (now.weekday() in [3,4,5] and meal == "dinner")):
    filtered_halls["Fac Shack"] = f"Closed for {meal}"
  #diana
  if now.weekday() == 5 or (now.weekday() == 6 and meal == "breakfast") or (now.weekday() == 4 and meal == "dinner"):
    filtered_halls["Diana"] = f"Closed for {meal}"
  #dummy_halls = dummy_food()

  #for each dining hall, skipping the closed ones, find each
  #station that's currently open and add it to the filtered dictionary
  for hall_name, stations in halls.items():
    if hall_name in filtered_halls and filtered_halls[hall_name].startswith("Closed"):
      continue
    filtered_stations = {}

    #this code will replace the below code once we have all scraped data.
    #here, we hard-code the times of each station of each dining hall.
    if hall_name == "John Jay" or hall_name == "Ferris":
      #filter for only open stations
      if meal == 'breakfast':
        for station, items in stations.get('breakfast',{}).items():
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
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"  
    if hall_name == "JJ's":
      #filter for only open stations
      if meal == 'breakfast':
        for station, items in stations.get('breakfast',{}).items():
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
      if meal == 'dinner':
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
      if len(filtered_stations) > 1:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"
    if hall_name == "Faculty House":
      #filter for only open stations
      if meal == 'lunch':
        for station, items in stations.get('lunch',{}).items():
            filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data" 
    if hall_name == "Chef Mike's":
      #filter for only open stations
      if meal == 'lunch' or meal == 'dinner':
        for station, items in stations.get('lunch & dinner',{}).items():
          filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"      
    if hall_name == "Chef Don's":
      if meal == 'breakfast':
        filtered_stations["Breakfast"] = ["Breakfast Sandwich"]
      if meal == 'lunch' or meal == 'dinner':
        filtered_stations["Pizza"] = ["Build your own"]
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"    
    if hall_name == "Grace Dodge":
      #filter for only open stations
      if meal == 'lunch' or meal == 'dinner':
        for station, items in stations.get('lunch & dinner',{}).items():
          filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"
    if hall_name == "Fac Shack":
      if meal == 'lunch':
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      if meal == 'dinner':
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"
    if hall_name == "Hewitt":
      if meal == 'breakfast':
        for station, items in stations.get('breakfast',{}).items():
          filtered_stations[station] = items
      if meal == 'lunch':
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      if meal == 'dinner':
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
      for station, items in stations.get('every day',{}).items():
        filtered_stations[station] = items
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"
    if hall_name == "Diana":
      if meal == 'breakfast':
        for station, items in stations.get('breakfast',{}).items():
          filtered_stations[station] = items
      if meal == 'lunch':
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      if meal == 'dinner':
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
        for station, items in stations.get('late night',{}).items():
          filtered_stations[station] = items
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"
    #old code for dummy case
    '''
    for station_name, station_info in stations.items():
      meals = station_info["meals"]
      if meal in meals:
        filtered_stations[station_name] = station_info["items"]
    if filtered_stations:
      filtered_halls[hall_name] = filtered_stations
    else:
      filtered_halls[hall_name] = "Missing Data"
    '''
  
  return filtered_halls

#mapping URLs to functions that display the HTML we want for that URL
@app.route('/') 
def index():
  filtered_halls = current_open_stations() # returns closed/missing data/meal info for each dining hall
  return render_template('index.html', halls=filtered_halls)
    
@app.route('/breakfast')
def breakfast():
  filtered_halls = open_at_meal("breakfast")
  return render_template('index.html', halls=filtered_halls, meal="breakfast")

@app.route('/lunch')
def lunch():
  filtered_halls = open_at_meal("lunch")
  return render_template('index.html', halls=filtered_halls, meal="lunch")

@app.route('/dinner')
def dinner():
  filtered_halls = open_at_meal("dinner")
  return render_template('index.html', halls=filtered_halls, meal="dinner")

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5000)