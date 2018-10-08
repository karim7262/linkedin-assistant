from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from client import LIClient
from settings import search_keys
import time



if __name__ == "__main__":
    
    # initialize LinkedIn web client
    chrome_options = Options() 
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = '/usr/bin/google-chrome'  
    #driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    liclient = LIClient(driver)
    
    
    driver.get("https://www.linkedin.com/uas/login")
    liclient.login()
    liclient.navigate_to_jobs_page()
    liclient.enter_search_keys()
    liclient.adjust_results_view()
    liclient.navigate_search_results()
    liclient.save_results()

    liclient.driver_quit()
    