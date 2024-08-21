from flask import *
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import random

app = Flask(__name__)
@app.route('/')
# this does the scraping and converts what is scraped into variables that can be displayed using HTML/CSS/Js
# Barnard pages need to be scraped separately. Those sites are shit, so need to figure out sm else 

def index():
  # options = webdriver.ChromeOptions()
  # options.headless = True
  driver = webdriver.Chrome(service=ChromeService( 
    ChromeDriverManager().install())) 

  cu_urls = ["https://dining.columbia.edu/content/john-jay-dining-hall","https://dining.columbia.edu/content/jjs-place-0", "https://dining.columbia.edu/content/ferris-booth-commons-0", "https://dining.columbia.edu/content/faculty-house-0", "https://dining.columbia.edu/chef-mikes", "https://dining.columbia.edu/content/chef-dons-pizza-pi", "https://dining.columbia.edu/content/grace-dodge-dining-hall-0", "https://dining.columbia.edu/content/fac-shack"]

  halls = {}

  for url in cu_urls:
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    title = driver.title
    print(title)
    time.sleep(random.uniform(2,5))

  driver.quit()
  return render_template('index.html', halls=halls)

if __name__ == '__main__':
   app.run(debug=True)

"""
try:
      closed_div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-ng-repeat="displayed_hours in hours.displayed_hours"][data-ng-bind="displayed_hours.title"]')))
      if "Closed" or "closed" in closed_div.text.strip():
          halls[title] = "Closed"
          continue
    except:
        pass

    items = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'meal-items')))
    title = driver.title 
    
    stations = driver.find_elements(By.CSS_SELECTOR, 'h2.station-title.ng-binding')
    # n = 0
    food_items = {}

    for index, item in enumerate(items):
      station = stations[index].text
      meals = item.find_elements(By.CSS_SELECTOR, 'h5.meal-title.ng-binding')
      food_items[station] = [m.text for m in meals]
        
      halls[title] = food_items
      time.sleep(random.uniform(2,5))
"""