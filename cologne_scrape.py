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
    
    #col2 scrapes column for sillage/longevity 
    col=soup.find('div',{'id':'col1'})
    col1=col.find('div',{'class':'effect6'})
    pyramid=col1.find_all('p')
    #col=col.find_all('span')
    user_pyramid=col1.find('div',{'id':'userMainNotes'})
    user_pyramid=user_pyramid.attrs['title']
    col2=col.find('div',{'class':'longSilBox effect6'})
    col2=col2.find_all('table')
    
    #notes of frag by product description
    top_notes=[]
    top_notes_id=[]
    mid_notes=[]
    mid_notes_id=[]
    base_notes=[]
    base_notes_id=[]

    for i in range(len(pyramid)):
        for j in range(len(pyramid[i].find_all('span',{'class':'rtgNote'}))):
            if i ==0:
                top_notes.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].find('img').attrs['title'])
                top_notes_id.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].attrs['title'])
            elif i ==1:
                mid_notes.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].find('img').attrs['title'])
                mid_notes_id.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].attrs['title'])
            else:
                base_notes.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].find('img').attrs['title'])
                base_notes_id.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].attrs['title'])
                
    #user voted strength of notes
    user_voted_pyramid=user_pyramid.split(';')
    
    #sillage
    sillage=col2[1].text.split()[2:]
    close_to_skin=sillage[1]
    radiates_arm_length=sillage[3]
    radiates_6ft=sillage[5]
    fills_room=sillage[7]
    
    #Longevity
    longevity=col2[0].text.split()[2:]
    longevity_30m_1hr=longevity[1]
    longevity_1hr_2hr=longevity[3]
    longevity_3hr_6hr=longevity[5]
    longevity_7hr_12hr=longevity[8]
    longevity_above12hr=longevity[12]
    
    reminds_me=col.find('div',{'class':'votes'})
    reminds_me.find('div',{'class':'fl'})
    remind=reminds_me.find_all('img')
    remind_value=reminds_me.find_all('span')
    
    #similiar fragrences voted by the public
    voted_similar_frag=[]
    for i in range(len(remind)):
        voted_similar_frag.append(remind[i].attrs['title'])
        voted_similar_frag.append(remind_value[i].text)
    
    #user reviews
    user_reviews={}
    user_review_date=[]
    for i in range(len(user)):
        user_name=user[i].find('div',{'class':'avatar'}).find('span').text.split('\n')[0]
        user_review=user[i].find('div',{'class':'revND'}).text.replace('\n','')
        user_reviews[user_name]=user_review
        user_review_date.append(user[i].find('div',{'class':'revND'}).text.split('\n')[1][1:])

    
    
    
    
    
    