# CologneRecommender
## Flask App to recommend and personalize fragrences given true user preferences. 
### Python - MongoDB - AWS - BeautifulSoup - Selenium - Flask - Bootstrap

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






Blind Buy gives the users multiple ways to help the recommendation system best cater their fragrence to their liking. It starts with the user creating an account and answering a short quiz. The quiz helps us recommend perfumes to people with no purchase history. Here Blind Buy uses a <b>Content-Based Recommender</b> using a weighted cosine similarity. 

Blind Buy gives the user the opportunity to rate other perfumes they have tried in the past. Here Blind Buy uses a <b>Collaborative Filtering Recommender</b> where users can ask for a specific type of fragrence through the fragrence test and also be recommended fragrences that other users similiar to them have also loved.






<img alt="" src='g.png' height='400px' width='500px' align='right'>



## Data Preparation



<details>
  <summary>
    <b> Gathering URLs </b>  
  </summary>
  
```python



```
</details>



<details>
    <summary>FPL</summary>
    <img alt="f" src='d.png'>
</details>




<br>

pass

<br>




<p>Model</p>
<br>
<p>RMSE</p>

<br>
<p><i> <b>Precision: </b> p </i></p>
<p><i> <b>Recall: </b> r </i></p>
<p><i> <b>F1-Score: </b> f1 </i></p>
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
- [x] Read
- [ ] 1
- [ ] 2
- [ ] 3