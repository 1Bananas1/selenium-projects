import time, sys, os
from bs4 import BeautifulSoup
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import logininfo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils.prediction import load_model, make_prediction
from utils.data_logger import log_result
from utils.countdown import countdown
from utils.getStat import getStat
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

model = load_model('covid_predictor.pkl')

USER = logininfo.getUser()
PASS = logininfo.getPass()
test_option = ['//*[@id="test"]','//*[@id="notest"]']
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

driver.get('https://www.gamelytics.net/covid-19-testing-game.html')
input_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "wsite-page-membership-text-input"))
)
input_element.send_keys(USER + Keys.TAB + PASS + Keys.ENTER)
input_element = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.XPATH,'//*[@id="test"]'))
)
consecutive_failure = 0
output = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="output"]')))
for j in range(30):
            output.send_keys(Keys.DOWN)


for test in range(10000):
        gender = getStat(driver,gender='gender')
        asthma = getStat(driver,asthma='asthma')
        fever = getStat(driver,fever='fever')

        prediction = make_prediction(model, gender, asthma, fever)

        if prediction:
                test_selected = test_option[0]
        else:
                test_selected = test_option[1]

        test_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,test_selected)))
        test_driver.click()



        #submit
        submit_driver = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="621061147342728456"]/input[9]')))
        submit_driver.click()

        status = getStat(driver,status='status')