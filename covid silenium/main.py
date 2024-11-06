import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import os
from logininfo import *

consecutive_failure = 0
tests = 100

USER = getUser()
PASS = getPass()

testlocs = ['//*[@id="test"]','//*[@id="notest"]']
submit_button = ['//*[@id="621061147342728456"]/input[9]']

day = 1
max_days = 31

def countdown(seconds):
  """Displays a countdown timer in minutes and seconds."""
  minutes_left = seconds // 60
  seconds_left = seconds % 60
  while seconds > 0:
    print(f"\n \n \n Site Down for Maintenance \n \n \n Time remaining: {minutes_left} minutes {seconds_left} seconds \n\n\n\n\n\n")
    time.sleep(1)
    seconds -= 1
    minutes_left = seconds // 60
    seconds_left = seconds % 60

for i in range(tests):
    print('Test: ' + str(i) +'/'+ str(tests))
    print(f'Consecutive Errors: {consecutive_failure}')
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service,options=options)
    driver.maximize_window()

    try:
        # Navigate to the webpage
        driver.get("https://www.gamelytics.net/covid-19-testing-game.html")
        # Wait for the input element for username and password to be present
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wsite-page-membership-text-input"))
        )
        # Send keys to the input element
        input_element.send_keys(USER + Keys.TAB + PASS + Keys.ENTER)
        input_element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,testlocs[0]))
        )
        consecutive_failure = 0

        for day in range(1,max_days):
           
            test_button_driver = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,testlocs[0])))
            test_button_driver.click()
            
            submit_button_driver = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,submit_button[0])))
            submit_button_driver.click()

        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())  # Wait for alert
            alert = driver.switch_to.alert  # Switch to alert
            alert.accept()
            download = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="621061147342728456"]/button'))
                )
            download.click()
            time.sleep(2)
        except Exception as e:
            print("No alert present or error occurred:", e)
    except Exception as e:
        print(f'Error has occured: {e}')
        consecutive_failure += 1
        if consecutive_failure == 3:
            print('\n \n \n Site Down for Maintenance \n \n \n')
            countdown(300)
            consecutive_failure = 0
        driver.quit()