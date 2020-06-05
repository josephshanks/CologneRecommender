import pandas as pd
import numpy as np
from pymongo import MongoClient
from bs4 import BeautifulSoup
import pprint
# Requests sends and recieves HTTP requests.
import requests
import warnings
import time
warnings.filterwarnings('ignore')

def main():
    df=pd.read_csv('data/men_urls.csv')
    for i in df['0']:
        frag_info_scrape(i)


def frag_info_scrape(url):
    '''
    INPUT(String) URL of fragrence review page for a specific fragrence
    '''
    client = MongoClient('localhost', 27017)
    db = client['cologne']
    mens_cologne = db['mens_cologne']
    
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
    try:
        image=mainpicbox.find('img')
        image=image.attrs['src']
    except:
        image=np.nan
    
    
    
    #have it, want it, had it, signature fragrence
    try:
        have_had_want=mainpicbox.find_all('p')[2].text
        have_had_want=have_had_want.split('  ')
    except:
        have_had_want=mainpicbox.find_all('p')[1].text
        have_had_want=have_had_want.split('  ')
    else:
        pass
    try:
        have_it=int(have_had_want[0].split()[3])
    except:
        have_it=0
    try:
        had_it=int(have_had_want[1].split()[3])
    except:
        had_it=0
    try:
        want_it=int(have_had_want[2].split()[3])
    except:
        want_it=0
    try:
        signature=int(have_had_want[3].split()[2])
    except:
        signature=0
    
    #price of frag
    prices=[]
    try:
        price=soup.find("div",{"id": "newsocial"})
        price=price.find_all('b')
        for p in price:
            prices.append(p.text)
    except:
        pass
    
    #description of frag
    try:
        description=soup.find('div',{'itemprop':'description'}).text
    except:
        description=''
    
    #col2 scrapes column for sillage/longevity
    col=soup.find('div',{'id':'col1'})
    col1=col.find('div',{'class':'effect6'})
    pyramid=col1.find_all('p')

    
    try:
        user_pyramid=col1.find('div',{'id':'userMainNotes'})
        user_pyramid=user_pyramid.attrs['title']
    except:
        user_pyramid=np.nan
        
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
            try:
                if i ==0:
                    top_notes.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].find('img').attrs['title'])
                    top_notes_id.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].attrs['title'])
            except:
                continue
            try:
                if i ==1:
                    mid_notes.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].find('img').attrs['title'])
                    mid_notes_id.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].attrs['title'])
            except:
                continue
            try:
                if i==2:
                    base_notes.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].find('img').attrs['title'])
                    base_notes_id.append(pyramid[i].find_all('span',{'class':'rtgNote'})[j].attrs['title'])
            except:
                continue
                
    #user voted strength of notes
    try:
        user_voted_pyramid=user_pyramid.split(';')
    except:
        user_voted_pyramid=np.nan
    
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
    
    #similiar fragrences voted by the public
    voted_similar_frag=[]
    try:
        reminds_me=col.find('div',{'class':'votes'})
        #reminds_me.find('div',{'class':'fl'})
        remind=reminds_me.find_all('img')
        remind_value=reminds_me.find_all('span')

        for i in range(len(remind)):
            voted_similar_frag.append(remind[i].attrs['title'])
            voted_similar_frag.append(remind_value[i].text)
    except:
        pass
    
    #user reviews
    
    user_reviews={}
    user_review_date=[]
    try:
        user=col.find_all('div',{'class':'pwq'})
        for i in range(len(user)):
            user_name=user[i].find('div',{'class':'avatar'}).find('span').text.split('\n')[0]
                if '.' in user_name:
                    user_name=user_name.replace('.',' ')
            user_review=user[i].find('div',{'class':'revND'}).text.replace('\n','')
            user_reviews[user_name]=user_review
            user_review_date.append(user[i].find('div',{'class':'revND'}).text.split('\n')[1][1:])
    except:
        pass
    

        
    mens_cologne.insert_one({
    'name': name, 
    'frag rating': frag_rating, 
    'main accords': accord_dic,
    'image':image,
    'have it':have_it,
    'had it':had_it,
    'want it':want_it,
    'signature':signature,
    'price':prices,
    'description':description,
    'top notes':top_notes,
    'top notes id':top_notes_id,
    'mid notes':mid_notes,
    'mid notes id':mid_notes_id,
    'base notes':base_notes,
    'base notes id':base_notes_id,
    'user voted notes': user_voted_pyramid,
    'close to skin':close_to_skin,
    'radiates about arm length':radiates_arm_length,
    'radiates 6ft':radiates_6ft,
    'fills room':fills_room,
    '30min to 1hr':longevity_30m_1hr,
    '1hr to 2hr':longevity_1hr_2hr,
    '3hr to 6hr':longevity_3hr_6hr,
    '7hr to 12hr':longevity_7hr_12hr,
    'greater than 12hr':longevity_above12hr,
    'similiar fragrences by user vote':voted_similar_frag,
    'user reviews':user_reviews,
    'user review date':user_review_date})
    
    time.sleep(11)
        
if __name__ == '__main__':
    main()

    
    
    
    
    
    