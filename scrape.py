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
import os
import platform
import json
import boto3
from barnard_scrape import scrape_barnard

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

    #determine OS and set chrome binary location based on that
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use the new headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

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
    title = driver.title
    dining_hall_name = title.split("|")
    print(dining_hall_name[0].lower())

    #let page load
    wait = WebDriverWait(driver, 40)

    #handle the privacy notice
    try:
      #accept_button = wait.until(
        #EC.element_to_be_clickable((By.XPATH, "//div[@id='cu-privacy-notice']//button[text()='I AGREE']"))
      #)
      #accept_button.click()
      iframe = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
      )
      print("privacy notice iframe detected")
      '''
      driver.switch_to.frame(iframe)
      possible_texts = ["i agree", "agree", "accept", "ok", "yes"]
      accept_buttons = driver.find_elements(By.TAG_NAME, "button")
      clicked = False
      for btn in accept_buttons:
        btn_text = btn.text.strip().lower()
        if btn_text in possible_texts:
          try:
            #btn.click()
            driver.execute_script("arguments[0].scrollIntoView();", btn) #scroll into view
            driver.execute_script("arguments[0].click();", btn) #the same as btn.click() but better?
            print(f"Clicked '{btn.text}' button to accept privacy notice.")
            clicked = True
            break
          except Exception as e:
            print(f"failed to click {btn.text} button. {e}")
      if not clicked:
        print("no accept button found on the privacy notice that was detected. attempting javascript dismissal")
        driver.switch_to.default_content()
        driver.execute_script("document.getElementById('cu-privacy-notice').style.display = 'none';")
        print("javascript removal successful")
      driver.switch_to.default_content()'''
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

#stores scraped data in a json file
def scrape_and_save():
  data = scrape_all()
  with open('dining_data.json', 'w') as f:
    json.dump(data, f, indent=4)
  upload_to_s3('dining_data.json', 'liondine-data')


def upload_to_s3(file_path, bucket_name, object_name=None):
  if object_name is None:
    object_name = os.path.basename(file_path)
  s3_client = boto3.client('s3')
  try:
    s3_client.upload_file(file_path, bucket_name, object_name)
    print(f"Data uploaded to S3 bucket '{bucket_name}' successfully.")
  except Exception as e:
     print(f"Failed to upload to S3: {e}")

if __name__ == '__main__':
   scrape_and_save()
   print("scraping and upload completed")
