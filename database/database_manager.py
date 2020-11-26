import logging
import sys
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from database.config import SQL_URL
from models import album
from models.album import Album, Artist, Label, Style, Mood, Theme, Track, ReviewBody, Base, Genre
from scraping.album import Album

logger = logging.getLogger('database_manager')
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_engine():
    return create_engine(SQL_URL, echo=True)


def create_databse():
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url)


def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)

   # engine = create_engine('mysql+mysqlconnector://root:?????????@localhost/dballmusic')




def drop_tables():
    engine = create_engine(SQL_URL, echo=True)
    Base.metadata.drop_all(engine)


def sql_session():
    engine = sql_engine()
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


def sql_engine():
    engine = create_engine(SQL_URL, echo=True)
    return engine


def insert(albums: List[Album]):
    session = sql_session()
    album_models = []
    for album in albums:
        artist = get_or_create(session, Artist, name=album.artist_name.name)
        label = Label(name=album.label.name)
        styles = [Style(description=style) for style in album.details.styles]
        moods = [Mood(description=mood) for mood in album.details.moods]
        themes = [Theme(description=theme) for theme in album.details.themes]
        genre = Genre(description=album.details.genre)
        tracks = [Track(title=track.get('title'), duration=track.get('duration')) for track in
                  album.details.track_listing]
        review_body = ReviewBody(content=album.details.review_body)
        model_album = ModelAlbum(reference_number=album.reference_number,
                                 title=album.title,
                                 artist=artist,
                                 label=label,
                                 genre=genre,
                                 headline_review_author=album.headline_review.author)
        session.add(model_album)
        session.commit()
