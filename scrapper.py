from bs4 import BeautifulSoup as soup
import requests
import numpy as np
import re
import pandas as pd
from requests.api import head


def get_ratings():
    """
    This funtion fetches best 1000 movies in terms of IMDB ratings.
    Returns a pandas dataframe like;
    ====================================================
                              Movie Title  Year  Rating
    0            The Shawshank Redemption  1994     9.3
    1                       The Godfather  1972     9.2
    ..                                ...   ...     ...
    ====================================================
    """
    # Requesting the page
    start_list = list(np.arange(0,2)*100+1) # list = [1, 101, 201, 301, 401, 501, 601, 701, 801, 901]

    headers = {"user-agent":"Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18"}
    responds = []
    for num in start_list: 
        url = f"https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start={num}&ref_=adv_nxt"
        responds.append(requests.get(url,headers=headers))
    
    # Scraping the content

    main_list = []

    for respond in responds:
        bsobj = soup(respond.content,'lxml')
        data_movies = bsobj.find_all('div',{'class':'lister-list'})[0].find_all('h3',{'class':'lister-item-header'})
        data_ratings = bsobj.find_all('div',{'class':'lister-list'})[0].find_all('div',{'class':'ratings-bar'})

        # Scraping the names
        movie_titles = [data.a.string for data in data_movies]
        
        # Scraping the years
        movie_years = [data.find_all("span",{"class":"lister-item-year text-muted unbold"})[0].string for data in data_movies]
        movie_years = [int(re.findall("[0-9]{4}",text)[0]) for text in movie_years]

        # Scraping the ratings
        movie_ratings = [float(data.strong.string) for data in data_ratings]

        current_list = list(zip(movie_titles,movie_years,movie_ratings))
        main_list = main_list + current_list

    return pd.DataFrame(main_list,columns=["Movie Title","Year","Rating"])