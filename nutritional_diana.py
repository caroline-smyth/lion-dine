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
from kosher_scrape import scrape_kosher
from selenium.webdriver.common.action_chains import ActionChains
import platform

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument("--headless=new")  # Run headless for efficiency
  chrome_options.add_argument("--headless=chrome")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--window-size=1920x1080")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--disable-blink-features=AutomationControlled")
  chrome_options.add_argument("--user-agent=Mozilla/5.0 ...")
  chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
  chrome_options.add_experimental_option("useAutomationExtension", False)
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
  return driver

def scrape_diana():
  hall_name = "Diana"
  driver = get_driver()
  url = "https://dineoncampus.com/barnard/whats-on-the-menu"
  driver.get(url)
  dining_hall_data = {}
  wait = WebDriverWait(driver, 40)


  driver.get(url)
  driver.save_screenshot("nutritional.png")
  dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn")))
  driver.execute_script("arguments[0].click();", dropdown)
  time_module.sleep(2)
  dropdown_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-menu.show")))

  items = dropdown_menu.find_elements(By.TAG_NAME, "button")
  for item in items:
    hall = item.text.strip()
    
    if hall_name in hall:
      item.click()
      hall_data = scrape_diana_inside(driver, wait)
      if hall_data is None:
        dining_hall_data[hall] = {}
      dining_hall_data[hall] = hall_data
  
  try:
    kosher_data = scrape_kosher()
    hewitt_kosher_data = kosher_data["Kosher"]
    for meal_time in hewitt_kosher_data:
      if "Hewitt Dining" not in dining_hall_data:
        dining_hall_data["Hewitt Dining"] = {}

    if meal_time in dining_hall_data["Hewitt Dining"]:
      dining_hall_data["Hewitt Dining"][meal_time].update(hewitt_kosher_data[meal_time])
  except:
    pass

    #print(dining_hall_data)
  driver.quit()
  return dining_hall_data

def scrape_diana_inside(driver, wait): 
  dining_hall = {}
  
  try:
    nav_bar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nav.nav-tabs")))

    buttons = nav_bar.find_elements(By.CLASS_NAME, "nav-link")

    for b in buttons:
      meal_time = b.text.strip().lower()
      meal = {}
      b.click()
      menu_elements = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "table")))


      for m in menu_elements:
        station_name = m.find_element(By.TAG_NAME, "caption").text.strip()
        icon_map = {
          "https://dineoncampus.com/img/icon_vegetarian.png": "Vegetarian", 
          "https://dineoncampus.com/img/icon_protein.png": "Protein Rich",
          "https://dineoncampus.com/img/icon_avoiding_gluten.png":"Gluten Free",
          "https://dineoncampus.com/img/icon_vegan.png":"Vegan",
          "https://dineoncampus.com/img/howgood-climate-friendly-new.png":"Climate"
        }

        table_element = driver.find_element(By.TAG_NAME, "tbody")
        rows = table_element.find_elements(By.TAG_NAME, "tr")
        station_foods = []
        for row in rows:
          food_name = row.find_element(By.TAG_NAME, "strong").text.strip()
          images = row.find_elements(By.TAG_NAME, "img")
          preferences = []
          for image in images:
            src = image.get_attribute("src")
            if src in icon_map:
              #print(icon_map[src])
              preferences.append(icon_map[src])
            
          food_info = {"title": food_name, "preferences": preferences, "allergens": None}
          #print(food_info)
          station_foods.append(food_info)
    
        meal[station_name] = station_foods
      dining_hall[meal_time] = meal
      print(dining_hall)
 
  except Exception as e:
    print(f"Error occurred: {e}")
    dining_hall = None
  print(dining_hall)
  return dining_hall

scrape_diana()