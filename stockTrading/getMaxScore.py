
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
import math

total_score = 0

USER = logininfo.getUser()
PASS = logininfo.getPass()

max_score = 27.4

maxscore_dir = os.path.join(current, "max_scores")  # Creates a 'downloads' folder in current directory
if not os.path.exists(maxscore_dir):
    os.makedirs(maxscore_dir)

chromeOptions = Options()
arguments = [
    "--disable-extensions",
    "--disable-notifications",
    "--disable-infobars",
    "--disable-popup-blocking",
    "--blink-settings=imagesEnabled=false",
    "--force-device-scale-factor=0.9"
]
chromeOptions.add_experimental_option("prefs", {
    "download.default_directory": maxscore_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

for arg in arguments:
    chromeOptions.add_argument(arg)
    
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)




max_days = 31
tests = 100000
gameOptions = ['//*[@id="buy"]','//*[@id="sell"]','//*[@id="678114044831709836"]/input[6]']

def getStat(driver, **kw):
    
    """Retrieve dynamically updated value on the page."""
    keywords = ['percentreturn','score','day']
    if len(kw) != 1:
        raise ValueError('getStat expects exactly one key argument')
    
    keyword = list(kw.keys())[0]
    if keyword not in keywords:
        raise ValueError(f'Invalid getStat keyword. Expected one of: {keywords}')

    try:
        # Try to retrieve the value using different approaches
        stat_value = driver.execute_script(f"""
            var elem = document.querySelector('#{keyword}');
            return elem ? (elem.value || elem.innerText || elem.textContent || '').trim() : '';
        """)
        
        # Check if the value is empty or whitespace
        if not stat_value:
            raise ValueError(f"No value found for '{keyword}'.")
        
        return stat_value
    except Exception as e:
        raise ValueError(f"Could not retrieve stat value for {keyword}. Error: {e}")
    


test_option = ['//*[@id="buy"]','//*[@id="sell"]']
    
    
consecutive_failure = 0
rollingAveragePercent = 0

try:
        # Navigate to the webpage
        driver.get('https://www.gamelytics.net/stock-trading-game.html')
        # Wait for the input element for username and password to be present
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wsite-page-membership-text-input"))
        )
        # Send keys to the input element
        input_element.send_keys(USER + Keys.TAB + PASS + Keys.ENTER)
        input_element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="buy"]'))
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
            time.sleep(30)
            consecutive_failure = 0
        driver.quit()

rolling_avg = []
for test in range(tests):
    rolling_avg.clear()
    boughtStatus = False
    time.sleep(0.00125)
    print('Test ' + str(test) + ' / ' + str(tests))
    if test == 0:
        optionSelected = gameOptions[0]
        optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
        optionDriver.click()
        optionSelected = gameOptions[2]
        optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
        optionDriver.click()
        boughtStatus = True
        # print('bought day 0')

    
    # print('Actual day: ',getStat(driver,day='day'))
    
    # print()

    for day in range(1,max_days):
        # print('Day: ',day)
        # print('Actual day: ',getStat(driver,day='day'))
        try:
            percentreturn = float(getStat(driver,percentreturn='percentreturn').strip('%'))
            # print(percentreturn)
            rolling_avg.append(percentreturn)
            if len(rolling_avg) > 3:
                 rolling_avg.pop(0)
            if len(rolling_avg) == 3:
                rollingAveragePercent = (math.fsum(rolling_avg) / 3)
            # print('rolling avg percent: ',rollingAveragePercent)
        except ValueError as ve:
            print(f"Error getting stat value: {ve}")

        

        if boughtStatus == True:
            if percentreturn >= 2 or percentreturn >= rollingAveragePercent + 1.1:
                optionSelected = gameOptions[1]
                optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
                optionDriver.click()
                if day != 30:
                    optionSelected = gameOptions[2]
                    optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
                    optionDriver.click()
                    boughtStatus = False
                    # print('sold')
            else:
                if day != 30:
                    optionSelected = gameOptions[2]
                    optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
                    optionDriver.click()
                    # print('kept')
        else:
            if percentreturn <= -2 or percentreturn <= rollingAveragePercent - 1.1:
                optionSelected = gameOptions[0]
                optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
                optionDriver.click()
                if day != 30:
                    optionSelected = gameOptions[2]
                    optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
                    optionDriver.click()
                    boughtStatus = True
                    # print('bought')
            else:
                if day != 30:
                    optionSelected = gameOptions[2]
                    optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
                    optionDriver.click()
                    # print('kept')
        
        
    
    currentScore = float(getStat(driver,score='score'))
    print('Current Test Score: ',currentScore)
    total_score += currentScore
    # print('Actual day: ',getStat(driver,day='day'))
    if currentScore > max_score:
         max_score = currentScore
         driver.save_screenshot(f"C:/Users/jmacd/OneDrive - Saint Louis University/coding 2 large/btm3700/seleniumProjects/stockTrading/max_scores/{max_score}_screenshot.png")

    print(f'Total Testing Average: {total_score / (test + 1):.2f}')
    print()

    
    
    optionSelected = gameOptions[2]
    optionDriver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,optionSelected)))
    optionDriver.click()
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())  # Wait for alert
        alert = driver.switch_to.alert
        alert.accept()
    except Exception as e:
         print('Error: ',e)
    
    


    