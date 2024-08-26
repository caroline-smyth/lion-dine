from flask import Flask, render_template
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time 
import time as time_module
import random

app = Flask(__name__) #sets up a flask application
cache = Cache(app, config={'CACHE_TYPE': 'simple'}) #sets up a cache for daily scraped data

#dining hall URLs
cu_urls = [
  "https://dining.columbia.edu/content/john-jay-dining-hall",
  "https://dining.columbia.edu/content/jjs-place-0", 
  "https://dining.columbia.edu/content/ferris-booth-commons-0",
  "https://dining.columbia.edu/content/faculty-house-0", 
  "https://dining.columbia.edu/chef-mikes", 
  "https://dining.columbia.edu/content/chef-dons-pizza-pi", 
  "https://dining.columbia.edu/content/grace-dodge-dining-hall-0", 
  "https://dining.columbia.edu/content/fac-shack"
  ]
  

# this does the scraping and converts what is scraped into variables that can be displayed using HTML/CSS/Js
# Barnard pages need to be scraped separately. Those sites are shit, so need to figure out sm else 
def scrape_data(url):
  # options = webdriver.ChromeOptions()
  # options.headless = True
  # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
  driver = webdriver.Chrome()
  halls = {}
 
  #for url in cu_urls:

  # open a URL, let it load, and find the name of the dining hall
  driver.get(url)
  wait = WebDriverWait(driver, 60)
  title = driver.title

  try:

    hall_name = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "node-title.ng-binding")))
    name = hall_name.text.strip()

    print(name)
    div_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cu-dining-location-description.ng-binding")))

    p_elements = div_element.find_elements(By.TAG_NAME, "p")

    p_texts = [p.text.strip() for p in p_elements]
    print(p_texts)

    # halls[name] = p_texts

  except:
    print("entered except")
  """
  this should go in try 
  #i think items and stations holds all the data?
  items = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'meal-items')))
  
  stations = driver.find_elements(By.CSS_SELECTOR, 'h2.station-title.ng-binding')
  #food_items = {"breakfast": [], "lunch": [], "dinner": []} 
  food_items = {} 

  #fill in the dictionary of (stations -> list of food items)
  for index, item in enumerate(items):
    station = stations[index].text
    meals = item.find_elements(By.CSS_SELECTOR, 'h5.meal-title.ng-binding')
    food_items[station] = [meal.text for meal in meals]
  
  #record the dictionary of all stations and items for this dining hall
  halls[title] = food_items
  """
  time_module.sleep(random.uniform(2,5)) #random sleep for anti-detection

  driver.quit()
  cache.set('halls_data', halls)

def dummy_food():
  #filling a dictionary to look like what a real halls dictionary would be.
  #using this to populate index.html

  johnjayfood={ 
    "Wilma's Grill": {"items": ["Pancakes", "Waffles", "Omelettes"], "hours":(time(9,30), time(14,0))},
    "Pasta Station": {"items": ["Cavatappi", "Whole Wheat Penne", "Marinara Sauce", "Parmesan Cheese"], "hours": (time(14,0), time(21,0))},
    "Main Line": {"items":["Chicken", "Asparagus", "Wild Rice"], "hours":(time(14,0), time(21,0))},
    "Dessert": {"items":["Lemon Pie", "Assorted Cookies", "Chocolate Pudding"], "hours":(time(14,0), time(21,0))}
  }
  jjsfood={
    "Grill Station": {"items":["Burgers", "Grilled Cheese"],"hours":(time(0,0), time(23,59))},
    "Custom Line": {"items":["Pancakes", "French Toast", "Eggs"],"hours":(time(0,0), time(23,59))},
    "Grab and Go": {"items":["Mozzerella Sticks", "Dino Nuggets", "Onion Rings"],"hours":(time(0,0),time(23,59))}
  }
  ferrisfood={
    "Main Line":{"items":["Apple Pancakes", "Bacon", "Scrambled Eggs", "Hash Browns", "Gravy"], "hours":(time(7,30),time(14,0))},"Vegan Station":{"items":["Beyond Sausage", "JustEgg", "Beets"], "hours":(time(7,30),time(14,0))}, "Fusion Station":{"items":["Tuna Poke Bowl", "Chives", "Carrots", "Steamed Vegetables"], "hours":(time(14,0),time(17,0))},
    "action station": {"items":["chunky monkey dinner waffles"],"hours":(time(17,0),time(20,0))},
    "main line": {"items":["entree", "vegetable", "rice"],"hours":(time(17,0),time(20,0))}
  }
  fachousefood={
    "Main Line": {"items":["Salmon", "Corn Nuggets", "Rice", "Greek Salad"],"hours":(time(11,0),time(14,30))},
    "Dessert": {"items":["Chocolate Chip Cookies", "Brownies"],"hours":(time(11,0),time(14,30))}
  }
  mikesfood={
    "Hot": {"items":["Buffalo Chicken"],"hours":(time(10,30),time(22,0))},
    "Hot Vegan": {"items":["Vegan Buffalo Chicken"],"hours":(time(10,30),time(22,0))},
    "Cold": {"items":["Prosciutto and Fig"],"hours":(time(10,30),time(22,0))},
    "Cold Vegan": {"items":["Portobello Mushroom"],"hours":(time(10,30),time(22,0))},
  }
  donsfood={
    "Breakfast": {"items":["Bacon Egg and Cheese Sandwich"],"hours":(time(8,0),time(11,0))},
    "Pizza": {"items":["Margarita", "Pepperoni"],"hours":(time(11,0),time(18,0))}
  }
  dodgefood={
    "Grab and Go": {"items":["Ramen Bowl"],"hours":(time(11,0),time(18,0))}
  }
  facshackfood={
    "Food": {"items":["Chicken Tikka Masala", "Chana Masala"],"hours":(time(11,0),time(14,30))}
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

def closed_missing_filter():
  now = datetime.now()
  halls = cache.get('halls_data') #get the already-scraped data
  if not halls: #if the scraping didn't work, scrape now
    for url in cu_urls:
      scrape_data(url)
    halls = cache.get('halls_data')
  filtered_halls = {}
  # CHECKS FOR CLOSED
  # john jay
  if now.weekday() in [4,5] or now.hour < 9 or now.hour >= 21 or (now.hour == 9 and now.minute < 30):
    filtered_halls["John Jay"] = "Closed"
  #jjs
  if now.hour in [10,11]:
    filtered_halls["JJ's"] = "Closed"
  #ferris
  if ((now.weekday() in [0,4] and (now.hour < 7 or now.hour >= 20 or (now.hour == 7 and now.minute < 30))) or
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
  
  dummy_halls = dummy_food()

  for hall_name, stations in dummy_halls.items():
    if hall_name in filtered_halls and filtered_halls[hall_name] == "Closed":
      continue
    filtered_stations = {}
    for station_name, station_info in stations.items():
      open_time, close_time = station_info["hours"]
      if open_time <= now.time() <= close_time:
        filtered_stations[station_name] = station_info["items"]
      if filtered_stations:
        filtered_halls[hall_name] = filtered_stations
      else:
        filtered_halls[hall_name] = "Missing Data"
  
  return filtered_halls

@app.route('/') #maps the URL / to index()
def index():
  filtered_halls = closed_missing_filter() # returns closed/missing data/meal info for each dining hall
    
  return render_template('index.html', halls=filtered_halls)
    
@app.route('/breakfast')
def breakfast():
  filtered_halls = closed_missing_filter()
  return render_template('breakfast.html', halls=filtered_halls)

@app.route('/lunch')
def lunch():
  filtered_halls = closed_missing_filter()
  return render_template('lunch.html', halls=filtered_halls)

@app.route('/dinner')
def dinner():
  filtered_halls = closed_missing_filter()
  return render_template('dinner.html', halls=filtered_halls)

# this schedules scraping to happen at midnight
def schedule_scraping():
  scheduler = BackgroundScheduler()
  for url in cu_urls:
    scheduler.add_job(scrape_data, trigger='cron', hour=0, minute=0, args=[url])
  scheduler.start()

if __name__ == '__main__':
   schedule_scraping()
   app.run(debug=True)

