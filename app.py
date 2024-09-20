from flask import Flask, render_template
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time 
import time as time_module
import random
from contextlib import contextmanager
import os

app = Flask(__name__) #sets up a flask application
cache = Cache(app, config={'CACHE_TYPE': 'simple'}) #sets up a cache for daily scraped data

#dining hall URLs and names 
cu_urls = {
  "John Jay" : "https://dining.columbia.edu/content/john-jay-dining-hall",
  "JJ's" : "https://dining.columbia.edu/content/jjs-place-0", 
  "Ferris" : "https://dining.columbia.edu/content/ferris-booth-commons-0",
  "Faculty House" : "https://dining.columbia.edu/content/faculty-house-0", 
  "Chef Mike's" : "https://dining.columbia.edu/chef-mikes",
  "Chef Don's" : "https://dining.columbia.edu/content/chef-dons-pizza-pi",
  "Grace Dodge" : "https://dining.columbia.edu/content/grace-dodge-dining-hall-0", 
  "Fac Shack" : "https://dining.columbia.edu/content/fac-shack"
}
hall_names = [
  "John Jay", 
  "JJ's", 
  "Ferris", 
  "Faculty House", 
  "Chef Mike's", 
  "Chef Don's", 
  "Grace Dodge", 
  "Fac Shack", 
  "Hewitt", 
  "Diana"
  ]

#configures webdriver for a headless environment
@contextmanager
def managed_webdriver():
  chrome_options = Options()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN", "/usr/bin/chromium")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  driver = webdriver.Chrome(options=chrome_options)
  try:
    yield driver
  finally:
    driver.quit()

#IN PROGRESS 
def scrape_barnard():
  with managed_webdriver() as driver:
    barnard_hall_names = ["Hewitt Dining", "Diana"]
    url = "https://dineoncampus.com/barnard/whats-on-the-menu"
    driver.get(url)
    dining_hall_data = {}
    wait = WebDriverWait(driver, 40)

    for hall_name in barnard_hall_names:
      # driver.get(url) # untested
      dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn")))
      dropdown.click()
      
      dropdown_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-menu.show")))

      items = dropdown_menu.find_elements(By.TAG_NAME, "button")
      for item in items:
        hall = item.text.strip()
        #print("inside loop " + hall)
        
        if hall_name in hall:
          item.click()
          #print("clicked " + hall)
          hall_data = scrape_barnard_inside(driver, wait)
          retries = 0
          while hall_data is None and retries < 4:
            time_module.sleep(2)
            hall_data = scrape_barnard_inside(driver, wait)
            retries += 1

          if hall_data is not None:
            dining_hall_data[hall] = hall_data
          else:
            print(f"Failed to scrape data for {hall}")
          
    print(dining_hall_data)
    return dining_hall_data

#IN PROGRESS
def scrape_barnard_inside(driver, wait): 
  dining_hall = {}
  
  try:
    nav_bar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nav.nav-tabs")))

    #print("entered try")

    buttons = nav_bar.find_elements(By.CLASS_NAME, "nav-link")

    for b in buttons:
      meal_time = b.text.strip().lower()
      meal = {}
      b.click()
      """
      try: potential try catch
        menu_elements = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "table")))
      except TimeoutException:
        print(f"Timeout occured while scraping {meal_time}")
        return None
        """
      menu_elements = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "table")))

      for m in menu_elements:
        station_name = m.find_element(By.TAG_NAME, "caption").text.strip()
        food_elements = m.find_elements(By.TAG_NAME, "strong")
        foods = [food.text.strip() for food in food_elements]
    
        meal[station_name] = foods
      dining_hall[meal_time] = meal

  except Exception as e:
    print(f"Error occurred: {e}")
    dining_hall = None # maybe return None

  return dining_hall

#returns a dictionary of the form {dining hall : {station : [items]}}
def scrape_columbia(hall_name):
  with managed_webdriver() as driver:
    url = cu_urls[hall_name]
    driver.get(url)
    title = driver.title
    dining_hall = title.split("|")
    print(dining_hall[0].lower())

    wait = WebDriverWait(driver, 40)

    buttons = driver.find_elements(By.TAG_NAME, "button")

    clicks = []

    for b in buttons:
      text = b.text.strip()
      if text == "Breakfast" or text == "Lunch" or text == "Dinner" or text == "Lunch & Dinner" or text == "Late Night":
        clicks.append(b)

    dining_hall = {}
    for button in clicks:
      button.click()
      meal = button.text.strip().lower()
      # print(meal)
      
      meal_dictionary = {}

      wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "wrapper")))

      station_elements = driver.find_elements(By.CLASS_NAME, "wrapper")

      for s in station_elements:
        station_name = s.find_element(By.CLASS_NAME, "station-title").text.strip()

        meal_items = s.find_elements(By.CLASS_NAME, "meal-title")

        meal_dictionary[station_name] = [item.text.strip() for item in meal_items]

        dining_hall[meal] = meal_dictionary

      print(dining_hall)

    return {hall_name : dining_hall}

#combines the columbia and barnard scrapes into one dictionary
def scrape_all():
  dict = {}
  for hall in cu_urls.keys():
    if hall == "Chef Don's":
      dict["Chef Don's"] = {'breakfast' : {}, 'lunch' : {}, 'dinner' : {}}
      continue
    hall_data = scrape_columbia(hall)
    dict.update(hall_data)
  barnard_data = scrape_barnard()
  dict.update(barnard_data)
  return dict

#for testing purposes to have food items to use without scraping
'''
def dummy_food():

  johnjayfood={ 
    "Wilma's Grill": {"items": ["Pancakes", "Waffles", "Omelettes"], "hours":(time(9,30), time(14,0)), "meals":["breakfast"]},
    "Pasta Station": {"items": ["Cavatappi", "Whole Wheat Penne", "Marinara Sauce", "Parmesan Cheese"], "hours": (time(14,0), time(21,0)),"meals":["lunch","dinner"]},
    "Main Line": {"items":["Chicken", "Asparagus", "Wild Rice"], "hours":(time(14,0), time(21,0)), "meals":["lunch","dinner"]},
    "Dessert": {"items":["Lemon Pie", "Assorted Cookies", "Chocolate Pudding"], "hours":(time(14,0), time(21,0)), "meals":["lunch","dinner"]}
  }
  jjsfood={
    "Grill Station": {"items":["Burgers", "Grilled Cheese"],"hours":(time(0,0), time(23,59)),"meals":["breakfast","lunch","dinner"]},
    "Custom Line": {"items":["Pancakes", "French Toast", "Eggs"],"hours":(time(0,0), time(23,59)),"meals":["breakfast","lunch","dinner"]},
    "Grab and Go": {"items":["Mozzerella Sticks", "Dino Nuggets", "Onion Rings"],"hours":(time(0,0),time(23,59)),"meals":["breakfast","lunch","dinner"]}
  }
  ferrisfood={
    "Main Line":{"items":["Apple Pancakes", "Bacon", "Scrambled Eggs", "Hash Browns", "Gravy"], "hours":(time(7,30),time(14,0)),"meals":["breakfast","lunch"]},
    "Vegan Station":{"items":["Beyond Sausage", "JustEgg", "Beets"], "hours":(time(7,30),time(14,0)),"meals":["breakfast","lunch"]}, 
    "Fusion Station":{"items":["Tuna Poke Bowl", "Chives", "Carrots", "Steamed Vegetables"], "hours":(time(14,0),time(17,0)),"meals":["lunch"]},
    "Action Station": {"items":["Chunky Monkey Dinner Waffles"],"hours":(time(17,0),time(20,0)),"meals":["dinner"]},
    "Main Line": {"items":["Chicken", "Green Beans", "Cornbread", "Rice"],"hours":(time(17,0),time(20,0)),"meals":["dinner"]}
  }
  fachousefood={
    "Main Line": {"items":["Salmon", "Corn Nuggets", "Rice", "Greek Salad"],"hours":(time(11,0),time(14,30)),"meals":["lunch"]},
    "Dessert": {"items":["Chocolate Chip Cookies", "Brownies"],"hours":(time(11,0),time(14,30)),"meals":["lunch"]}
  }
  mikesfood={
    "Hot": {"items":["Buffalo Chicken"],"hours":(time(10,30),time(22,0)),"meals":["lunch"]},
    "Hot Vegan": {"items":["Vegan Buffalo Chicken"],"hours":(time(10,30),time(22,0)),"meals":["lunch"]},
    "Cold": {"items":["Prosciutto and Fig"],"hours":(time(10,30),time(22,0)),"meals":["lunch"]},
    "Cold Vegan": {"items":["Portobello Mushroom"],"hours":(time(10,30),time(22,0)),"meals":["lunch"]},
  }
  donsfood={
    "Breakfast": {"items":["Bacon Egg and Cheese Sandwich"],"hours":(time(8,0),time(11,0)),"meals":["breakfast"]},
    "Pizza": {"items":["Margarita", "Pepperoni"],"hours":(time(11,0),time(18,0)),"meals":["lunch","dinner"]}
  }
  dodgefood={
    "Grab and Go": {"items":["Ramen Bowl"],"hours":(time(11,0),time(18,0)),"meals":["lunch","dinner"]}
  }
  facshackfood={
    "Lunch": {"items":["Chicken Tikka Masala", "Chana Masala"],"hours":(time(11,0),time(14,30)),"meals":["lunch"]}
  }
  
  dummy_halls = {
    "John Jay": johnjayfood,
    "JJ's": jjsfood,
    "Ferris": ferrisfood,
    "Faculty House": fachousefood,
    "Chef Mike's": mikesfood,
    "Chef Don's": donsfood,
    "Grace Dodge": dodgefood,
    "Fac Shack": facshackfood
  }

  return dummy_halls
  '''

#takes the dictionary of all food items and filters it to only include
#stations that are currently open
def current_open_stations():
  now = datetime.now()
  halls = cache.get('halls_data') #get the already-scraped data
  if not halls: #if the scraping didn't work, scrape now
    halls = scrape_all()
    cache.set('halls_data', halls)
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
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"
    
    if hall_name == "JJ's":
      #filter for only open stations
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
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"

    if hall_name == "Ferris":
      if now.weekday() in [0,1,2,3,4]:
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
      #if now.weekday() == 5:
        #do later
      if now.weekday() == 6:
        if now.hour >= 10 and now.hour < 2:
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
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"

    if hall_name == "Faculty House":
      #filter for only open stations
      for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"

    if hall_name == "Chef Mike's":
      #filter for only open stations
      for station, items in stations.get('lunch & dinner',{}).items():
        filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"      

    if hall_name == "Chef Don's":
      if now.hour >= 8 and now.hour < 11:
        filtered_stations["Breakfast"] = ["Breakfast Sandwich"]
      if now.hour >= 11 and now.hour < 18:
        filtered_stations["Pizza"] = ["Build your own"]
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"

    if hall_name == "Grace Dodge":
      #filter for only open stations
      for station, items in stations.get('lunch & dinner',{}).items():
        filtered_stations[station] = items
      #return data to the filtered dictionary
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"
    
    if hall_name == "Fac Shack":
      if now.weekday() in [0,1,2,3] and now.hour >= 11 and now.hour < 14:
        for station, items in stations.get('lunch',{}).items():
          filtered_stations[station] = items
      if now.weekday() in [3,4,5] and now.hour >= 19 and now.hour < 23:
        for station, items in stations.get('dinner',{}).items():
          filtered_stations[station] = items
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"

    if hall_name == "Hewitt":
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"
    if hall_name == "Diana":
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing data"
    

  
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
  halls = cache.get('halls_data') #get the already-scraped data
  if not halls: #if the scraping didn't work, scrape now
    halls = scrape_all()
    cache.set('halls_data', halls)
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
      if filtered_stations:
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
  #for url in cu_urls:
    #scrape_columbia(url)
  #scrape_barnard()
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

#schedules scraping to happen at midnight
def schedule_scraping():
  scheduler = BackgroundScheduler()
  scheduler.add_job(scrape_all, trigger='cron', hour=0, minute=0)
  scheduler.start()

if __name__ == '__main__':
   schedule_scraping()
   app.run(host='0.0.0.0', port=5000)

