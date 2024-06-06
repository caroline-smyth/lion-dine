from flask import *
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
@app.route('/')

# this does the scraping and converts what is scraped into variables that can be displayed using HTML/CSS/Js
# Barnard pages need to be scraped separately. Those sites are shit, so need to figure out sm else 

def index():
  options = webdriver.ChromeOptions()
  options.headless = True
  # here insert a check by seeing if "closed" is contained in hours possibly?
  driver = webdriver.Chrome(service=ChromeService( 
    ChromeDriverManager().install())) 

  cu_urls = ["https://dining.columbia.edu/content/john-jay-dining-hall", "https://dining.columbia.edu/content/jjs-place-0", "https://dining.columbia.edu/content/ferris-booth-commons-0", "https://dining.columbia.edu/content/faculty-house-0", "https://dining.columbia.edu/chef-mikes", "https://dining.columbia.edu/content/chef-dons-pizza-pi", "https://dining.columbia.edu/content/grace-dodge-dining-hall-0", "https://dining.columbia.edu/content/fac-shack"]

  halls = {}

  for url in cu_urls:
    driver.get(url)
    wait = WebDriverWait(driver, 60)
    
    items = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'meal-items')))
    title = driver.title 
    
    #title = driver.title
    #halls[title] = "No items"
    #print(f"Error processing {url}")
    #continue
    stations = driver.find_elements(By.CSS_SELECTOR, 'h2.station-title.ng-binding')
    # n = 0
    food_items = {}

    for index, item in enumerate(items):
        # print(stations[n].text)
        # halls.append(stations[n].text)
        # n += 1
        station = stations[index].text
        meals = item.find_elements(By.CSS_SELECTOR, 'h5.meal-title.ng-binding')
        food_items[station] = [m.text for m in meals]
        
        # for m in meal:
        #  print(m.text)
        #  halls.append(m.text)

        #print("\n")
    halls[title] = food_items

  driver.quit()
  return render_template('index.html', halls=halls)

if __name__ == '__main__':
   app.run(debug=True)
