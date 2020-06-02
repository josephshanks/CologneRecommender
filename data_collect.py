from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import warnings
warnings.filterwarnings('ignore')
options = Options()
options.headless = True
def frag_url_scrape(url):
    '''
    Scrapes all url's from fragrantica search
    
    Input(String): URLs from https://www.fragrantica.com/search/ 
                    Parameters may be set to however the user wants.
    
    Returns(List): URL of all colognes given the paramaters. MAX of 1000 fragrances
    '''
    
    #Start web driver

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    
    #Find xpath of the "show more results" button, click it repeatedly to show all results
        butt=driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[1]/div[1]/div/div/div/div[2]/div[1]/div/div[3]/div/div/div/div/div/button")
    elements = driver.find_elements_by_css_selector("div.ais-InfiniteHits a")
    WebDriverException()
    for i in range(1000):
        try:
            WebDriverException()
            butt.click()
        except:
            continue
    elements = driver.find_elements_by_css_selector("div.ais-InfiniteHits a")
    
    #collect url list
    urls=[]
    for elem in elements:
        urls.append(elem.get_attribute("href"))

    driver.quit()
    
    return urls

