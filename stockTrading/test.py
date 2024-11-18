from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time, sys, os
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import stats
from collections import deque
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import logininfo

class EnhancedTrader:
    def __init__(self):
        self.price_history = []
        self.return_history = []
        self.balance_history = []
        self.score_history = []
        self.ma_short = 3
        self.ma_long = 5
        self.volatility_window = 3
        self.momentum_threshold = 1.1
        self.trend_strength = 0
        self.boughtStatus = False
        self.consecutive_losses = 0
        self.max_consecutive_losses = 3

    def update_metrics(self, price, percent_return, balance, score):
        self.price_history.append(price)
        self.return_history.append(percent_return)
        self.balance_history.append(balance)
        self.score_history.append(score)
        
        if len(self.price_history) >= max(self.ma_long, self.volatility_window):
            self.calculate_trend_strength()

    def calculate_trend_strength(self):
        ma_short = np.mean(self.price_history[-self.ma_short:])
        ma_long = np.mean(self.price_history[-self.ma_long:])
        recent_volatility = np.std(self.return_history[-self.volatility_window:])
        price_momentum = (ma_short - ma_long) / ma_long
        self.trend_strength = price_momentum / recent_volatility if recent_volatility != 0 else 0

    def get_trading_decision(self, current_return):
        if len(self.price_history) < max(self.ma_long, self.volatility_window):
            return 'hold'
            
        # Check recent performance
        if len(self.score_history) > 1:
            if self.score_history[-1] < self.score_history[-2]:
                self.consecutive_losses += 1
            else:
                self.consecutive_losses = 0

        # More conservative if too many losses
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.momentum_threshold = 1.5  # More conservative threshold
        else:
            self.momentum_threshold = 1.1  # Normal threshold
            
        if self.boughtStatus:
            if (current_return >= 2.0 or 
                current_return >= self.momentum_threshold or
                (self.trend_strength < -0.5 and current_return > 0)):
                return 'sell'
        else:
            if (current_return <= -2.0 or 
                current_return <= -self.momentum_threshold or
                (self.trend_strength > 0.5 and current_return < 0)):
                return 'buy'
        
        return 'hold'

    def reset(self):
        self.__init__()

def getStat(driver, **kw):
    keywords = ['percentreturn', 'score', 'day', 'stockprice', 'balance']
    if len(kw) != 1:
        raise ValueError('getStat expects exactly one key argument')
    
    keyword = list(kw.keys())[0]
    if keyword not in keywords:
        raise ValueError(f'Invalid getStat keyword. Expected one of: {keywords}')

    try:
        stat_value = driver.execute_script(f"""
            var elem = document.querySelector('#{keyword}');
            return elem ? (elem.value || elem.innerText || elem.textContent || '').trim() : '';
        """)
        
        if not stat_value:
            raise ValueError(f"No value found for '{keyword}'.")
        
        return stat_value
    except Exception as e:
        raise ValueError(f"Could not retrieve stat value for {keyword}. Error: {e}")

def clear_output(driver):
    try:
        # Find and click the output text box
        output = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="output"]')))
        output.click()
        
        # Select all text and delete
        output.send_keys(Keys.CONTROL + "a")  # Select all text
        output.send_keys(Keys.BACK_SPACE)     # Delete selected text
        
    except Exception as e:
        print(f"Error clearing output: {e}")

def main():
    # Initialize variables
    total_score = 0
    max_score = 27.4
    max_days = 31
    tests = 100000
    USER = logininfo.getUser()
    PASS = logininfo.getPass()

    # Setup directories
    current = os.path.dirname(os.path.realpath(__file__))
    maxscore_dir = os.path.join(current, "max_scores")
    if not os.path.exists(maxscore_dir):
        os.makedirs(maxscore_dir)

    # Chrome setup
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
        
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                            options=chromeOptions)

    gameOptions = ['//*[@id="buy"]','//*[@id="sell"]',
                  '//*[@id="678114044831709836"]/input[6]']
    consecutive_failure = 0
    trader = EnhancedTrader()

    try:
        # Login
        driver.get('https://www.gamelytics.net/stock-trading-game.html')
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 
            "wsite-page-membership-text-input")))
        input_element.send_keys(USER + Keys.TAB + PASS + Keys.ENTER)
        
        input_element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="buy"]')))
        
        consecutive_failure = 0
        clear_output(driver)

        # Main testing loop
        for test in range(tests):
            if test > 0 and test % 20 == 0:  # Clear every 20 tests after first test
                clear_output(driver)
                time.sleep(0.1)
            time.sleep(0.00125)
            print('Test ' + str(test) + ' / ' + str(tests))
            
            # Reset trader for new test
            trader.reset()

            # Initial buy on day 1
            if test == 0:
                optionSelected = gameOptions[0]
                optionDriver = WebDriverWait(driver,10).until(
                    EC.element_to_be_clickable((By.XPATH,optionSelected)))
                optionDriver.click()
                optionSelected = gameOptions[2]
                optionDriver = WebDriverWait(driver,10).until(
                    EC.element_to_be_clickable((By.XPATH,optionSelected)))
                optionDriver.click()
                trader.boughtStatus = True

            # Daily trading loop
            for day in range(1, max_days):
                try:
                    # Get current stats
                    price = float(getStat(driver, stockprice='stockprice'))
                    percent_return = float(getStat(driver,
                                        percentreturn='percentreturn').strip('%'))
                    balance = float(getStat(driver, balance='balance'))
                    score = float(getStat(driver, score='score'))
                    
                    # Update trader metrics and get decision
                    trader.update_metrics(price, percent_return, balance, score)
                    decision = trader.get_trading_decision(percent_return)
                    
                    # Execute trading decision
                    if decision == 'buy' and not trader.boughtStatus:
                        optionSelected = gameOptions[0]
                        optionDriver = WebDriverWait(driver,10).until(
                            EC.element_to_be_clickable((By.XPATH,optionSelected)))
                        optionDriver.click()
                        trader.boughtStatus = True
                    elif decision == 'sell' and trader.boughtStatus:
                        optionSelected = gameOptions[1]
                        optionDriver = WebDriverWait(driver,10).until(
                            EC.element_to_be_clickable((By.XPATH,optionSelected)))
                        optionDriver.click()
                        trader.boughtStatus = False

                    # Move to next day if not last day
                    if day != 30:
                        optionSelected = gameOptions[2]
                        optionDriver = WebDriverWait(driver,10).until(
                            EC.element_to_be_clickable((By.XPATH,optionSelected)))
                        optionDriver.click()
                        
                except ValueError as ve:
                    print(f"Error getting stat value: {ve}")

            # End of test handling
            currentScore = float(getStat(driver,score='score'))
            print('Current Test Score: ',currentScore)
            total_score += currentScore
            
            if currentScore > max_score:
                max_score = currentScore
                driver.save_screenshot(
                    f"{maxscore_dir}/{max_score}_screenshot.png")

            print(f'Total Testing Average: {total_score / (test + 1):.2f}')
            print()

            # Reset for next test
            optionSelected = gameOptions[2]
            optionDriver = WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.XPATH,optionSelected)))
            optionDriver.click()
            
            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
            except Exception as e:
                print('Alert handling error: ', e)

    except Exception as e:
        print(f'Error has occurred: {e}')
        consecutive_failure += 1
        if consecutive_failure == 3:
            print('\n \n \n Site Down for Maintenance \n \n \n')
            time.sleep(30)
            consecutive_failure = 0
        driver.quit()

if __name__ == "__main__":
    main()