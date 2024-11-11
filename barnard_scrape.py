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

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument("--headless")  # Run headless for efficiency
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--window-size=1920x1080")
  driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
  return driver

def scrape_barnard():
  barnard_hall_names = ["Hewitt Dining"]
  #barnard_hall_names = ["Diana Center Cafe"]
  driver = get_driver()
  url = "https://dineoncampus.com/barnard/whats-on-the-menu"
  driver.get(url)
  dining_hall_data = {}
  wait = WebDriverWait(driver, 40)

  for hall_name in barnard_hall_names:
    driver.get(url)
    dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn")))
    dropdown.click()
    
    dropdown_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-menu.show")))

    items = dropdown_menu.find_elements(By.TAG_NAME, "button")
    for item in items:
      hall = item.text.strip()
      
      if hall_name in hall:
        item.click()
        hall_data = scrape_barnard_inside(driver, wait)
        if hall_data is None:
          dining_hall_data[hall] = {}
        dining_hall_data[hall] = hall_data
    kosher_data = scrape_kosher()
    hewitt_kosher_data = kosher_data["Hewitt Kosher"]
    #print(hewitt_kosher_data)

    for meal_time in hewitt_kosher_data:
      #print("hiii " + meal_time)
      if "Hewitt Dining" not in dining_hall_data:
        dining_hall_data["Hewitt Dining"] = {}

      if meal_time in dining_hall_data["Hewitt Dining"]:
        dining_hall_data["Hewitt Dining"][meal_time].update(hewitt_kosher_data[meal_time])


    #print(dining_hall_data)
  driver.quit()
  return dining_hall_data

def scrape_barnard_inside(driver, wait): 
  dining_hall = {}
  
  try:
    nav_bar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nav.nav-tabs")))

    buttons = nav_bar.find_elements(By.CLASS_NAME, "nav-link")

    for b in buttons:
      meal_time = b.text.strip().lower()
      meal = {}
      b.click()
      #time_module.sleep(1)
      menu_elements = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "table")))

      for m in menu_elements:
        station_name = m.find_element(By.TAG_NAME, "caption").text.strip()
        food_elements = m.find_elements(By.TAG_NAME, "strong")
        foods = [food.text.strip() for food in food_elements]
    
        meal[station_name] = foods
      dining_hall[meal_time] = meal
 
  except Exception as e:
    print(f"Error occurred: {e}")
    dining_hall = None

  #print(dining_hal
  return dining_hall

#scrape_barnard