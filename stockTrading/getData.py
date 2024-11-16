
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time, sys, os
from bs4 import BeautifulSoup
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import logininfo
import random



USER = logininfo.getUser()
PASS = logininfo.getPass()


download_dir = os.path.join(current, "downloads")  # Creates a 'downloads' folder in current directory
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

chromeOptions = Options()
arguments = [
    "--disable-extensions",
    "--disable-notifications",
    "--disable-infobars",
    "--disable-popup-blocking",
    "--blink-settings=imagesEnabled=false"
]
chromeOptions.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

for arg in arguments:
    chromeOptions.add_argument(arg)
    
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)

decisions = ['keep','sell']

max_days = 31
tests = 250
gameOptions = ['//*[@id="buy"]','//*[@id="sell"]','//*[@id="678114044831709836"]/input[6]']

try:
        # Navigate to the webpage
        driver.get('https://www.gamelytics.net/stock-trading-game.html')
        
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wsite-page-membership-text-input"))
        )
        # Send keys to the input element
        input_element.send_keys(USER + Keys.TAB + PASS + Keys.ENTER)
        input_element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="678114044831709836"]/input[6]'))
        )
        consecutive_failure = 0
        output = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="output"]')))
        for j in range(30):
                    output.send_keys(Keys.DOWN)
        
        

except Exception as e:
        print(f'Error has occured: {e}')
        consecutive_failure += 1
        if consecutive_failure == 3:
            print('\n \n \n Site Down for Maintenance \n \n \n')
            # countdown(300)
            consecutive_failure = 0
        driver.quit()


boughtStatus = False

for test in range(tests):
    print('Test: ' + str(test) +'/'+ str(tests))
    print(f'Consecutive Errors: {consecutive_failure}')
    boughtStatus = False
    # optionSelected = gameOptions[0]
    # optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
    # optionDriver.click()
    # optionSelected = gameOptions[2]
    # optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
    # optionDriver.click()
    # boughtStatus = True
    for day in range(1,max_days):
        if boughtStatus == True: # sell it
            optionSelected = gameOptions[1]
            optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
            optionDriver.click()
            optionSelected = gameOptions[2]
            optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
            optionDriver.click()
            boughtStatus = False
        else: # buy it
            optionSelected = gameOptions[0]
            optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
            optionDriver.click()
            optionSelected = gameOptions[2]
            optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
            optionDriver.click()
            boughtStatus = True
    try:
        optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
        optionDriver.click()
        WebDriverWait(driver, 5).until(EC.alert_is_present())  # Wait for alert
        alert = driver.switch_to.alert  # Switch to alert
        alert.accept()
        download = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="678114044831709836"]/button')))
        download.click()
        time.sleep(2)
    except Exception as e:
        try:
                download = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="678114044831709836"]/button')))
                download.click()
                time.sleep(2)
        except Exception as e:
                print("No alert present or error occurred:", e)
    
            
                  
           