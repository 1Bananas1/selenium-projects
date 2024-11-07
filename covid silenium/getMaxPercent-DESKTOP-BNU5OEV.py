
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
total_score = 0

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

USER = logininfo.getUser()
PASS = logininfo.getPass()
max_score = 90

chromeOptions = Options()
arguments = [
    "--disable-extensions",
    "--disable-notifications",
    "--disable-infobars",
    "--disable-popup-blocking",
    "--incognito",
    "--blink-settings=imagesEnabled=false"
]


for arg in arguments:
    chromeOptions.add_argument(arg)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)

max_days = 31
tests = 10000

def getStat(driver, **kw):
    
    """Retrieve dynamically updated value on the page."""
    keywords = ['gender', 'asthma', 'fever']
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



test_option = ['//*[@id="test"]','//*[@id="notest"]']
    
    
consecutive_failure = 0




try:
        # Navigate to the webpage
        driver.get('https://www.gamelytics.net/covid-19-testing-game.html')
        # Wait for the input element for username and password to be present
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "wsite-page-membership-text-input"))
        )
        # Send keys to the input element
        input_element.send_keys(USER + Keys.TAB + PASS + Keys.ENTER)
        input_element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="test"]'))
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
            countdown(300)
            consecutive_failure = 0
        driver.quit()


# asthma = getStat(driver,asthma='asthma')

for test in range(tests):
    if max_score == 100:
        quit
    time.sleep(0.00125)
    print('Test ' + str(test) + ' / ' + str(tests))
    for day in range(1, max_days):
        try:
            asthma = getStat(driver, asthma='asthma')
            gender = getStat(driver, gender='gender')
            fever = int(getStat(driver, fever='fever').strip())  # Stripping whitespace for good measure
        except ValueError as ve:
            print(f"Error getting stat value: {ve}")
            fever = None  # Assign a default or skip this iteration as needed

        # if fever is not None:
        #     print('Day: ' + str(day) + ' | Asthma: ' + asthma + ' |  Gender: ' + gender + ' | Fever: ' + str(fever))
        # print()
        
        if gender == 'male':
            if asthma == 'yes': # most males with asthma dont have it
                if fever >= 102:
                    # has covid!! 
                    test_selected = test_option[0]
                    test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                    test_driver.click()
                else:
                    # no covid
                    test_selected = test_option[1]
                    test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                    test_driver.click()

            elif asthma == 'no':
                if fever >= 101:
                    # has covid!
                    test_selected = test_option[0]
                    test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                    test_driver.click()
                    
                else:
                    #no covid
                    test_selected = test_option[1]
                    test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                    test_driver.click()
                    

            elif asthma == 'unknown':
                # prob has covid sorry bud
                test_selected = test_option[0]
                test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                test_driver.click()
                


        elif gender == 'female':
            if asthma == 'unknown':
                test_selected = test_option[0]
                test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                test_driver.click()
                # likely covid

            elif asthma == 'no':
                if fever >= 100:
                    test_selected = test_option[0]
                    test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                    test_driver.click()
                    # covid!
                else:
                    test_selected = test_option[1]
                    test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                    test_driver.click() 
                    # no covid
                


            elif asthma == 'yes':
                if fever >= 102:
                    test_selected = test_option[0]
                    test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                    test_driver.click()
                    # covid!
                else:
                    test_selected = test_option[1]
                    test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
                    test_driver.click()
                    # no covid
        
        submit_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="621061147342728456"]/input[9]')))
        submit_driver.click()

    # try:
    WebDriverWait(driver, 5).until(EC.alert_is_present())  # Wait for alert
    alert = driver.switch_to.alert  # Switch to alert
    
    testing_accuracy = int(alert.text.split("accuracy of ")[1].rstrip("%!"))
    total_score += testing_accuracy
    # print(average_impressions)
    
    if testing_accuracy > max_score:
        max_score = testing_accuracy
        alert.accept()
        
        driver.save_screenshot(f"C:/Users/jmacd/OneDrive - Saint Louis University/coding 2 large/btm3700/seleniumProjects/covid silenium/output/{max_score}_LAPTOPscreenshot.png")

        time.sleep(2)
        
    else:
        print(f'Average: {total_score / (test + 1):.2f}%')
        alert.accept()  
    print()
    # except Exception as e:
    #     print("No alert present or error occurred:", e)
