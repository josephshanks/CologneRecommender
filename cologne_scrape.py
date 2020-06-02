import pandas as pd
import numpy as np
from pymongo import MongoClient
from bs4 import BeautifulSoup
import pprint
# Requests sends and recieves HTTP requests.
import requests
import warnings
warnings.filterwarnings('ignore')

def frag_info_scrape(url):
    '''
    INPUT(String) URL of fragrence review page for a specific fragrence
    '''
    
    
    r=requests.get(url, headers = {'User-agent': 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})
    soup = BeautifulSoup(r.content, "html.parser")
    
    name=soup.find("div",{"id": "col1"})
    name=name.find_all("span",{'itemprop':'name'})
    name[1].text
    
    