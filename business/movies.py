import requests
from bs4 import BeautifulSoup
from database import Movie


def get_movie_info(movie_url):
    URL = f"https://filmow.com{movie_url}"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html5lib")

    return soup


def format_movie_info(soup):
    movie_info = soup.find(
        "div",
        attrs={"class": "span9"},
    )

    movie_id = int(
        movie_info.find("div", attrs={"class": "star-rating"})["data-movie-pk"]
    )

    movie_name = movie_info.find("h1", attrs={"itemprop": "name"}).get_text(strip=True)

    movie_rating = float(
        movie_info.find("span", attrs={"class": "average"}).get_text(strip=True)
    )

    movie = Movie(
        id=movie_id,
        title=movie_name,
        rating=movie_rating,
    )

    return movie
