import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
import time

MOVIES_TO_ADD = Path("movie_urls/movies_to_add")


def get_number_of_comments(movie):
    number_of_comments = movie.find(
        "span", attrs={"class": "badge badge-num-comments tip"}
    ).get_text(strip=True)

    if "K" in number_of_comments:
        number_of_comments = (
            float(number_of_comments.strip("K").replace(",", ".")) * 1000
        )
    number_of_comments = int(number_of_comments)

    return number_of_comments


def get_movie_links():
    for page in range(1, 4106):
        URL = f"https://filmow.com/filmes-todos/?pagina={page}"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html5lib")

        movies_table = soup.find(
            "ul",
            attrs={"id": "movies-list"},
        )

        movie_urls = []
        for movie in movies_table.findAll(
            "li", attrs={"class": "movie_list_item movie-list__container-movie"}
        ):
            number_of_comments = get_number_of_comments(movie)

            if number_of_comments >= 300:
                movie_url = movie.a["href"]
                movie_urls.append(movie_url)

        if movie_urls:
            filename = f"{page}.txt"
            with open(MOVIES_TO_ADD / filename, "w") as f:
                f.write(" ".join(movie_urls))

            time.sleep(3)


def get_movie_urls(file):
    with open(file, "r") as file:
        movie_urls = file.read().split()
    return movie_urls
