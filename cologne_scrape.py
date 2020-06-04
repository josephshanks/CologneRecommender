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
    
    #test for 200 status
    print(r.status_code)
    
    #name of frag
    name=soup.find("div",{"id": "col1"})
    name=name.find_all("span",{'itemprop':'name'})
    name=name[1].text
    
    #user ratings of the frag by demographic/time of day/season
    ratings = soup.find("div", {"id": "diagramresult"})
    rating=ratings.attrs['title']
    rating=rating.split(':')
    
    #dic of ratings - keys:type of rating - values:number of votes
    frag_rating={}
    for idx,data in enumerate(rating[:-1]):
        if idx % 2 == 0:
            frag_rating[data]=float(rating[idx+1])
        else:
            continue
    
    #unique accord dictionaries - Key()
    accords=soup.find("div",{"id": "prettyPhotoGallery"})
    accords=accords.find_all('div')
    accord_dic={}
    for i in [2,5,8,11,14,17]:
        try:
            key=accords[i].find('span').text
            value=accords[i].find('div').attrs['style']
            value=value.split(';')[0].split(': ')[1].split('p')[0]
            accord_dic[key]=float(value)
        except:
            pass
    
    mainpicbox=soup.find("div",{"id": "mainpicbox"})
    
    #image of frag
    image=mainpicbox.find('img')
    image=image.attrs['src']
    
    #have it, want it, had it, signature fragrence
    have_had_want=mainpicbox.find_all('p')[2].text
    have_had_want=have_had_want.split('  ')
    have_it=int(have_had_want[0][-4:])
    had_it=int(have_had_want[1][-4:])
    want_it=int(have_had_want[2][-4:])
    signature=int(have_had_want[3][-4:])
    
    #price of frag
    price=soup.find("div",{"id": "newsocial"})
    price=price.find_all('b')
    prices=[]
    for p in price:
        prices.append(p.text)
    
    #description of frag
    description=soup.find('div',{'itemprop':'description'}).text
    

    
    
    
    
    
    