# CologneRecommender
## Flask App to recommend and personalize fragrences given true user preferences. 
Python - MongoDB - AWS - BeautifulSoup - Selenium - Flask - Bootstrap

7/13/2020 Flask app in progress....

<img alt="B" src='e.png' height="600px" width="1000px" align='center'>



## Table of Contents

- [Overview](#overview)
- [Workflow](#workflow)
    - [Data Scraping](#data-scraping)
    - [Data Cleaning]
    - [Normalize]
    - [EDA]
    - [NLP Sentiment Analysis]
- [Models](#models)
- [Results](#results)
- [Validating it Works](#validating-it-works)
- [Tools and Packages Used](#tools-and-packages-used)
- [Future Work](#future-work)

## Overview

There are so many factors as to why I believe a fragrence recommendation app is a neccessity its hard to pick where to start. So first, a little background on the perfume industry. According to [Grand View Research Inc.](https://www.prnewswire.com/news-releases/fragrance-market-size-worth-91-17-billion-by-2025--cagr-3-7-grand-view-research-inc-300875093.html#:~:text=Home%20Fragrance%20Market%20%E2%80%93%20The%20global,3.9%25%20from%202019%20to%202025) the global perfume/cologne market value was at a whopping 31.4 Billion in 2018. Surely you might not be surprised at this number when you see hollywood actors and supermodels being used as advertisements for just about every single designer fragrence released. 

Within the fragrence "community" there are two buckets in which a fragrence could fall under - The designer fragrences or the niche fragrences. Designer fragrences are the fragrences you might pick up when you walk into your local Nordstrom or Macy's, think of brands such as Chanel, YSL, or Gorgio Armani. Niche fragrences span accross thousands of different houses that can range from your local candle shop to companies such as Creed (Creed was recently purchased with an estimated revenue of 200 million dollars). Just within the last few years did the niche fragrences actually outsell the designer fragrences proving that the fragrence market is shifting towards wanting more personalized, high quality products. According to Grand View Research, sales of celebrity perfumes such as David Beckham or Ariana Grande have declined by 22% since 2016. The consumers are no longer swayed by low quality celebrity products and demand for quality and personalization.

<b>But what does quality and personalization mean?</b>

Sure you may prefer one fragrence over the next but that doesn't make for a quality fragrence. Here lies the rub. Extremely important factors are missing such as: longevity (how long does the perfume stay on my skin for?), or sillage (how far does the perfume project off my skin). Maybe I want a perfume specifically for the summer, or maybe for the fall. Maybe I want a perfume that is made for the office and not for a night out clubbing. What if I am older and need something more saphisticated? What if I am picky and love floral notes and hate leather notes? Maybe I don't care what I smell like at all and I am just looking to find a mass pleasing fragrence loved by 25-35 year old females specifically.

<b>These features (and more) listed above are the optimal solution to the cold start problem! Simply recommending fragrences based off note breakdown is NOT a recipe for retaining customers. Your recommender would point towards cheap knockoffs that smell like the original but extra synethic and with no longevity.</b> 

## Workflow




Blind Buy gives the users multiple ways to help the recommendation system best cater their fragrence to their liking. It starts with the user creating an account and answering a short quiz. The quiz helps us recommend perfumes to people with no purchase history. Here Blind Buy uses a <b>Content-Based Recommender</b> using a weighted cosine similarity. 

Blind Buy gives the user the opportunity to rate other perfumes they have tried in the past. Here Blind Buy uses a <b>Collaborative Filtering Recommender</b> where users can ask for a specific type of fragrence through the fragrence test and also be recommended fragrences that other users similiar to them have also loved.






<img alt="" src='g.png' height='400px' width='500px' align='right'>



## Data Scraping

Tools used: Selenium, BeautifulSoup

*picture of site*

To gather the data I used a combination of Selenium and BeautifulSoup. The webdriver was needed in order to systematically click a "show more" button on the cologne page. Because only about 20 fragrences were shown at once I needed an automated way to collect the url pages for each fragrence. 

<details>
  <summary>
    <b> Initial URL Scrape </b>  
  </summary>
  
```python
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

```
</details>

Once I gathered a list of all fragrence URL's I used BeautifulSoup to extract relevant data from each cologne page. BeautifulSoup tends to be quicker than Selenium and with the large amount of data I was gathering, computing time was a major factor. I then exported the URL's to a csv file to be used with BeautifulSoup.

A MongoDB database was also created within a Docker container to allow for my data to be stored. 

<details>
  <summary>
    <b> Cologne Scrape </b>  
  </summary>
  
```python
def frag_info_scrape(url):
    '''
    INPUT(String) URL of fragrence review page for a specific fragrence
    '''
#     client = MongoClient('localhost', 27017)
#     db = client['cologne']
#     mens_cologne = db['mens_cologne']
    
    r=requests.get(url, headers = {'User-agent': 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'})
    soup = BeautifulSoup(r.content, "html.parser")
    
    #test for 200 status
    print(r.status_code)
    
    #name of frag
    try:
        name=soup.find("div",{"id": "col1"})
        name=name.find_all("span",{'itemprop':'name'})
        name=name[1].text
    except:
        pass
    
    #user ratings of the frag by demographic/time of day/season
    try:
        ratings = soup.find("div", {"id": "diagramresult"})
        rating=ratings.attrs['title']
        rating=rating.split(':')
    except:
        pass
    
    #dic of ratings - keys:type of rating - values:number of votes
    frag_rating={}
    for idx,data in enumerate(rating[:-1]):
        if idx % 2 == 0:
            frag_rating[data]=float(rating[idx+1])
        else:
            continue
    
    #unique accord dictionaries - Key()
    try:
        accords=soup.find("div",{"id": "prettyPhotoGallery"})
        accords=accords.find_all('div')
    except:
        pass
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
    try:
        col=soup.find('div',{'id':'col1'})
        col1=col.find('div',{'class':'effect6'})
    except:
        pass
    try:
        pyramid=col1.find_all('p')
    except:
        pass
    
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
    

        
    mens.insert_one({
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

```
</details>


## Data Cleaning

During the webscraping process I discovered that the fragrence website HTML code was structured quite poorly making for an extremely messy dataset. I ended up creating numerous cleaning functions in order to simply unpack the different datatypes into a useable database for my models. You can find this code in the src folder. 

## Normalize

Many features in my dataset consisted of user voted data. Because some fragrences are rated numerous times and others rated once or twice, I decided to normalize the user voted data in order to avoid a bias towards the more popular fragrences. 

## EDA

## NLP Sentiment Analysis

There are two major types of recommendation models, one in which uses explicit data and one which uses implicit data. Unfortuntaely I actually had neither. Explicit data uses specific ratings for a product from a user such as "Bob rated Aqua Di Gio a 5/5", and implicit data uses other factors to determine interest in a product such as how many times a product was viewed or mentioned. Due to the fact I only had user reviews on the colognes (granted years worth of reviews) I decided to do a Natural Language Processing Sentiment Analysis. A sentiment analysis allowed for me to test for a threshold using a lexicon to 
produce a polarity score between 1-5 for each review. 

*picture of reviews

** how did i test for accuracy?

After more data wrangling, 

<p>Model</p>
<br>
<p>RMSE</p>

<br>
<p><i> <b>RMSE: </b> p </i></p>

<br>




<b>Graph </b>
    TESTTESTTESTETSTES     |         TESTTEST          |
:-------------------------:|:-------------------------:|
![test1](gd.png)| ![test2](gr.png) |
<br>
<p><i>New  </i></p>
<br>





<i>Note:</i>


<img alt="gif" src='flask.gif'>



<details>
    <summary>Test</summary>
    <img alt="mat" src='oo.gif'>
    <br>
    <i>The model</i>
</details>

## Future Work

- [ ] Flask
- [ ] Scrape Female and Unisex fragrences
- [x] 1
- [ ] 2
- [ ] 3