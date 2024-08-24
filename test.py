from flask import Flask, render_template
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
import time 
import random

app = Flask(__name__) #sets up a flask application
cache = Cache(app, config={'CACHE_TYPE': 'simple'}) #sets up a cache for daily scraped data

#dining hall URLs
cu_urls = [
  "https://dining.columbia.edu/content/john-jay-dining-hall", "https://dining.columbia.edu/content/jjs-place-0"]
""" 
  "https://dining.columbia.edu/content/jjs-place-0",
  "https://dining.columbia.edu/content/ferris-booth-commons-0",
  "https://dining.columbia.edu/content/faculty-house-0", 
  "https://dining.columbia.edu/chef-mikes", 
  "https://dining.columbia.edu/content/chef-dons-pizza-pi", 
  "https://dining.columbia.edu/content/grace-dodge-dining-hall-0", 
  "https://dining.columbia.edu/content/fac-shack"
  """
  

# this does the scraping and converts what is scraped into variables that can be displayed using HTML/CSS/Js
# Barnard pages need to be scraped separately. Those sites are shit, so need to figure out sm else 
def scrape_data():
  driver = webdriver.Chrome()
  halls = {}
 
  for url in cu_urls:

    # open a URL, let it load, and find the name of the dining hall
    driver.get(url)
    wait = WebDriverWait(driver, 60)
    title = driver.title

    # check if it's closed. this logic will have to change now that we're
    #doing one daily scraping, but i'm leaving it as placeholder for now.
    try:
      print("entered try")
      # playing with text element that's already on the screen
      
      random_text = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "node-title.ng-binding")))
      print(random_text.text)
        

    except:
      pass

    time.sleep(random.uniform(2,10)) #random sleep for anti-detection

  driver.quit()
  cache.set('halls_data', halls)


@app.route('/') #maps the URL / to index()
def index():
  halls = cache.get('halls_data') #get the already-scraped data
  if not halls: #if the scraping didn't work, scrape now
    scrape_data()
    halls = cache.get('halls_data')
  return render_template('index.html', halls=halls)
    
@app.route('/breakfast')
def breakfast():
  return render_template('breakfast.html')

@app.route('/lunch')
def lunch():
  return render_template('lunch.html')

@app.route('/dinner')
def dinner():
  return render_template('dinner.html')

#this schedules scraping to happen at midnight
def schedule_scraping():
  scheduler = BackgroundScheduler()
  scheduler.add_job(scrape_data, trigger='cron', hour=0, minute=0)
  scheduler.start()

if __name__ == '__main__':
   schedule_scraping()
   app.run(debug=True)

