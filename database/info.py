from database.models import Base, Movie, User, Rating, Comment, Comment_Info
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB = os.getenv("DB")

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

Base.metadata.create_all(engine)
