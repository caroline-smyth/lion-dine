#hello
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from datetime import datetime, time 
import time as time_module
import random
from contextlib import contextmanager
import uuid
import os
import platform
import json
import boto3
from barnard_scrape import scrape_barnard
from diana_scrape import scrape_diana
from kosher_scrape import scrape_kosher

#dining hall URLs and names 
"""
cu_urls = {
  "John Jay" : "https://dining.columbia.edu/content/john-jay-dining-hall",
  "JJ's" : "https://dining.columbia.edu/content/jjs-place-0", 
  "Ferris" : "https://dining.columbia.edu/content/ferris-booth-commons-0",
  "Faculty House" : "https://dining.columbia.edu/content/faculty-house-0", 
  "Chef Mike's" : "https://dining.columbia.edu/chef-mikes",
  "Chef Don's" : "https://dining.columbia.edu/content/chef-dons-pizza-pi",
  "Grace Dodge" : "https://dining.columbia.edu/content/grace-dodge-dining-hall-0", 
  "Fac Shack" : "https://dining.columbia.edu/content/fac-shack",
  "Johnny's": "https://dining.columbia.edu/johnnys" 
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
  "Hewitt Dining", 
  "Diana Center Cafe",
  ]
"""
cu_urls = {"Grace Dodge" : "https://dining.columbia.edu/content/grace-dodge-dining-hall-0"}
hall_names = ["Grace Dodge"]

#configures webdriver for a headless environment 
@contextmanager
def managed_webdriver():

    #determine OS and set chrome binary location based on that
    chrome_options = Options()
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use *new* headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    #anti-bots for headless mode
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    #user-agent?
    chrome_options.add_argument(
      "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/115.0.5790.102 Safari/537.36"
    )

    '''#replacement for headless? forces each run to use a fresh profile
    unique_profile = os.path.join("/tmp", f"chrome_profile_{uuid.uuid4().hex}")
    chrome_options.add_argument(f"--user-data-dir={unique_profile}")'''

    # Determine the OS and set Chrome binary location
    
    current_os = platform.system()
    
    if current_os == "Linux":
        chrome_options.binary_location = '/usr/bin/google-chrome'
    elif current_os == "Darwin":
        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif current_os == "Windows":
        chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    else:
        raise Exception(f"Unsupported OS: {current_os}")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        yield driver
    except WebDriverException as e:
        print(f"WebDriverException occurred: {e}")
    finally:
        try:
            driver.quit()
        except:
            print(f"Error quitting driver: {e}")


#returns a dictionary of the form {dining hall : {station : [items]}}
def scrape_columbia(hall_name):
  with managed_webdriver() as driver:

    #go to the URL and print the title of the page
    url = cu_urls[hall_name]
    driver.get(url)
    time_module.sleep(5)
    title = driver.title
    dining_hall_name = title.split("|")
    actual_name = dining_hall_name[0].lower()
    print(actual_name)

    #let page load
    wait = WebDriverWait(driver, 40)

    #handle the privacy notice
    try:
      iframe = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
      )
      print("privacy notice iframe detected")
      
      driver.execute_script("document.getElementById('cu-privacy-notice').style.display = 'none';")
      print("javascript removal successful")
    except TimeoutException:
      print("No privacy notice found or it didn't appear in time")
    except NoSuchElementException:
      print("Privacy notice elements not found")
    except ElementClickInterceptedException:
      print("Privacy notice could not be clicked. Attempting javascript dismissal.")
      try:
        driver.execute_script("document.getElementById('cu-privacy-notice').style.display = 'none';")
      except Exception as e:
        print(f"Unexpected error while handling privacy notice: {e}")
    except Exception as e:
      print(f"Unexpected error while handling privacy notice: {e}")

    #continue with scraping 
    driver.save_screenshot("debug_dropdown.png")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    meal_buttons = []

    for b in buttons:
      text = b.text.strip()
      if text in ["Breakfast", "Brunch", "Lunch", "Dinner", "Lunch & Dinner", "Late Night", "Daily"]:
        meal_buttons.append(b)

    dining_hall = {}
    for button in meal_buttons:
      button.click()
      meal = button.text.strip().lower()
      meal_dictionary = {}
      wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "wrapper")))
      station_elements = driver.find_elements(By.CLASS_NAME, "wrapper")
      driver.save_screenshot("debug2.png")
      for s in station_elements:
        station_name = s.find_element(By.CLASS_NAME, "station-title").text.strip()
        meal_items = s.find_elements(By.CLASS_NAME, "meal-title")
        meal_items_text = [item.text.strip() for item in meal_items]

        if "ferris" in actual_name:
          if "Action" in station_name or "Pizza" in station_name:
            try:
              meal_description = s.find_element(By.CLASS_NAME, "meal-description").text.strip()
              meal_items_text[0] = meal_items_text[0] + ": " + meal_description
              meal_dictionary[station_name] = meal_items_text[0]
            except:
              station_name = s.find_element(By.CLASS_NAME, "station-title").text.strip()
              meal_items = s.find_elements(By.CLASS_NAME, "meal-title")
              meal_items_text = [item.text.strip() for item in meal_items]

        if "chef mike's" in actual_name:
           if "Hot Counter" in station_name or "Cold Counter" in station_name:
              try:
                n = 0
                for item in meal_items:
                  meal_item = item.text.strip()
                  meal_descriptions = s.find_elements(By.CLASS_NAME, "meal-description")
                  meal_desc_text = [desc.text.strip() for desc in meal_descriptions]
                  meal_item = meal_item + ": " + meal_desc_text[n]
                  meal_items_text[n] = meal_item
                  n+=1
                meal_dictionary[station_name] = meal_items_text
                #print(meal_dictionary)
                
              except:
                station_name = s.find_element(By.CLASS_NAME, "station-title").text.strip()
                meal_items = s.find_elements(By.CLASS_NAME, "meal-title")
                meal_items_text = [item.text.strip() for item in meal_items]

        if "johnny" in actual_name:
          meal_descriptions = s.find_elements(By.CLASS_NAME, "meal-description")
          meal_descriptions_text = [desc.text.strip() for desc in meal_descriptions]
          combined_items = [element for pair in zip(meal_items_text, meal_descriptions_text) for element in pair]

          meal_dictionary[station_name] = combined_items
        elif "grace dodge" in actual_name:
          meal_descriptions = s.find_elements(By.CLASS_NAME, "meal-description")
          meal_descriptions_text = [desc.text.strip() for desc in meal_descriptions]
          meal_dictionary[station_name] = meal_descriptions_text
        else:
          meal_dictionary[station_name] = meal_items_text
      dining_hall[meal] = meal_dictionary

    #print(dining_hall)

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

  '''
  barnard_data = scrape_barnard()
  dict.update(barnard_data)
  diana_data = scrape_diana()
  dict.update(diana_data)
  print(dict)'''
  print(dict)
  return dict


#stores scraped data in a json file
def scrape_and_save():
  data = scrape_all()
  with open('dining_data.json', 'w') as f:
    json.dump(data, f, indent=4)
  #upload_to_s3('dining_data.json', 'liondine-data')


def upload_to_s3(file_path, bucket_name, object_name=None):
  if object_name is None:
    object_name = os.path.basename(file_path)
  #boto3 automatically looks for credentials stored locally
  s3_client = boto3.client('s3')
  try:
    s3_client.upload_file(file_path, bucket_name, object_name)
    print(f"Data uploaded to S3 bucket '{bucket_name}' successfully.")
  except Exception as e:
     print(f"Failed to upload to S3: {e}")

if __name__ == '__main__':
   scrape_and_save()
   print("scraping and upload completed")

