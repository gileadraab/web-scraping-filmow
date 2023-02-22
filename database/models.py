from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from dataclasses import dataclass


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    rating: Mapped[Optional[float]]

    def __repr__(self) -> str:
        return f"Movie(id={self.id!r}, title={self.title!r}, rating={self.rating!r})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"

    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )

    ratings = relationship(
        "Rating", back_populates="user", cascade="all, delete-orphan"
    )


class Rating(Base):
    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    rating: Mapped[Optional[float]]

    user = relationship("User", back_populates="ratings")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    comment: Mapped[str] = mapped_column(String())

    user = relationship("User", back_populates="comments")


@dataclass
class Comment_Info:
    user_id: int
    name: str
    username: str
    comment_id: int
    comment: str
    rating: Optional[float]
