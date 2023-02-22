import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from database import Comment, Comment_Info


def get_comments_raw_info(movie_url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    URL = f"https://filmow.com{movie_url}"
    driver.get(URL)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")

    comments_raw_info = soup.find(
        "ul",
        attrs={"class": "media-list comments-list"},
    )

    return comments_raw_info


def format_comments_info(comments_raw_info):
    comments_info = []

    for comment in comments_raw_info.findAll(
        "li", attrs={"class": "media comments-list-item"}
    ):
        comment_info = {}

        comment_info["user_id"] = int(
            comment.find("a", attrs={"class": "user-name tip-user"})["data-user-pk"]
        )

        comment_info["name"] = comment.find(
            "a", attrs={"class": "user-name tip-user"}
        ).get_text(strip=True)

        comment_info["username"] = (
            comment.find("a", attrs={"class": "user-name tip-user"})["href"]
            .replace("usuario", "")
            .replace("/", "")
        )

        user_rating = comment.find(
            "span", attrs={"class": "tip star-rating star-rating-small stars"}
        )
        if user_rating:
            comment_info["rating"] = float(user_rating["title"].split()[1])
        else:
            comment_info["rating"] = None

        comment_info["user_comment_id"] = int(comment["data-comment-pk"])

        user_comment = comment.find("p")
        if user_comment:
            comment_info["comment"] = user_comment.get_text(strip=True)
        else:
            comment_info[
                "comment"
            ] = "Usuário temporariamente bloqueado por infringir os termos de uso do Filmow."

        comment_info = Comment_Info(
            user_id=comment_info["user_id"],
            name=comment_info["name"],
            username=comment_info["username"],
            rating=comment_info["rating"],
            comment_id=comment_info["user_comment_id"],
            comment=comment_info["comment"],
        )
        comments_info.append(comment_info)
    return comments_info


def format_comment_info(comment_info, movie):
    comment = Comment(
        id=comment_info.comment_id,
        user_id=comment_info.user_id,
        movie_id=movie.id,
        comment=comment_info.comment,
    )
    return comment
