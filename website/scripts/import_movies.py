import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import django


from base.models import Movie
from django.db import transaction




def run():
    url = "https://www.imdb.com/search/title/?title_type=feature&genres=comedy"
    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_containers = soup.find_all("div", class_="sc-74bf520e-3 klvfeN dli-parent")
    data = []

    # extracting movie details
    for container in movie_containers:
        movie_data = {}
        movie_data['name'] = re.sub(r'\d+\.\s', '', container.find("h3", class_="ipc-title__text").text.strip())
        movie_data['year'] = container.find('div', class_='sc-b189961a-7 feoqjK dli-title-metadata').find_all('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item')[0].text.strip() if container.find('div', class_='sc-b189961a-7 feoqjK dli-title-metadata').find_all('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item') else "N/A"
        runtime_container = container.find('div', class_='sc-b189961a-7 feoqjK dli-title-metadata').find_all('span', class_='sc-b189961a-8 kLaxqf dli-title-metadata-item')
        movie_data['runtime'] = runtime_container[1].text.strip() if len(runtime_container) > 1 else "N/A"
        rating = container.find("span", class_="ipc-rating-star--base").text.strip() if container.find("span", class_="ipc-rating-star--base") else "N/A"
        movie_data['rating'] = rating.split('(')[0].strip() if rating else "N/A"
        movie_data['description'] = container.find("div", class_="ipc-html-content-inner-div").text.strip() if container.find("div", class_="ipc-html-content-inner-div") else "N/A"

        # Extracting movie URL
        movie_url_element = container.find("a", class_="ipc-lockup-overlay ipc-focusable")
        if movie_url_element:
            movie_url = "https://www.imdb.com" + movie_url_element.get("href", "")
            print("Movie URL:", movie_url)  # Print the movie URL for verification

            # Accessing movie page to get additional details
            movie_response = requests.get(movie_url, headers=headers)
            movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
            
            # Extracting additional details
            movie_data['image_url'] = movie_soup.find("meta", property="og:image").get("content", "") if movie_soup.find("meta", property="og:image") else "N/A"
            director_stars = movie_soup.find_all("a", class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
            movie_data['director'] = director_stars[0].text.strip() if director_stars else "N/A"
            movie_data['stars'] = ", ".join([star.text.strip() for star in director_stars[1:11]]) if len(director_stars) > 1 else "N/A"
        else:
            movie_data['image_url'] = "N/A"
            movie_data['director'] = "N/A"
            movie_data['stars'] = "N/A"
        data.append(movie_data)

    # Saving movies to database
    with transaction.atomic():       
        for movie_data in data:
            movie = Movie(
                title=movie_data['name'], 
                description=movie_data['description'],
                genre='comedy',  
                length=movie_data['runtime'],
                rating=movie_data['rating'],
                image_url=movie_data['image_url'],
                director=movie_data['director'],
                stars=movie_data['stars']
            )
            movie.save()

            