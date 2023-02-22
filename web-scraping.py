from database import Base, Movie, User, Rating, Comment, Comment_Info, engine
from business import (
    MOVIES_TO_ADD,
    get_movie_urls,
    get_movie_info,
    format_movie_info,
    get_comments_raw_info,
    format_comments_info,
    format_comment_info,
    format_user_info,
)
from sqlalchemy.orm import Session
import os
from pathlib import Path
import shutil

MOVIES_ADDED = Path("movie_urls/movies_added")


def add_movie_to_DB():
    with Session(engine) as session:
        for file in MOVIES_TO_ADD.glob("*.txt"):
            file_path = MOVIES_TO_ADD / os.path.basename(file)

            movie_urls = get_movie_urls(file)

            for movie_url in movie_urls:
                movie_info = get_movie_info(movie_url)
                movie = format_movie_info(movie_info)
                session.merge(movie)
                session.commit()
                print(movie)

                comments_raw_info = get_comments_raw_info(movie_url)
                comments_info = format_comments_info(comments_raw_info)

                for comment_info in comments_info:
                    user = format_user_info(comment_info)
                    session.merge(user)
                    session.commit()
                    comment = format_comment_info(comment_info, movie)
                    session.merge(comment)
                    session.commit()
            shutil.move(file_path, MOVIES_ADDED)
            print(f"{os.path.basename(file)} moved to MOVIES_ADDED")


add_movie_to_DB()
