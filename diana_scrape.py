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
  url = "https://dineoncampus.com/barnard/whats-on-the-menu"

  driver = get_driver()

  driver.get(url)
  dining_hall_data = {}
  wait = WebDriverWait(driver, 40)

  dropdown = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "btn")))
  #dropdown.click()
  driver.execute_script("arguments[0].click();", dropdown)
  
  dropdown_menu = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-menu.show")))
  
  hall_buttons = dropdown_menu.find_elements(By.TAG_NAME, "button")

  for h_button in hall_buttons:
    if hall_name in h_button.text.strip():
      time_module.sleep(5)
      h_button.click()
    else:
      continue
  hall_data = {}

  try:
    nav_bar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nav.nav-tabs")))
    buttons = nav_bar.find_elements(By.CLASS_NAME, "nav-link")
    meal_times = [btn.text.strip().lower() for btn in buttons]
    #print(meal_times)
    
    for b in buttons:
      meal_time = b.text.strip().lower()
      time_module.sleep(5)
      b.click()
      meal = {}
      nav_bar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".nav.nav-tabs")))
      buttons = nav_bar.find_elements(By.CSS_SELECTOR, ".nav-link")

      menu_elements = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME, "table")))

      for m in menu_elements:
        station_name = m.find_element(By.TAG_NAME, "caption").text.strip()
        food_elements = m.find_elements(By.TAG_NAME, "strong")
        foods = [food.text.strip() for food in food_elements]
    
        meal[station_name] = foods
      hall_data[meal_time] = meal

  except Exception as e:
    print(f"Error occurred: {e}")
    hall_data = None

  if hall_data is None:
    dining_hall_data["Diana"] = {}
  dining_hall_data["Diana"] = hall_data

  driver.quit()
  #print(dining_hall_data)
  return dining_hall_data
    
#scrape_diana()