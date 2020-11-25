import logging
import sys
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.config import SQL_URL
from models import album
from models.album import Album, Artist, Label, Style, Mood, Theme, Track, ReviewBody, Base, Genre
from scraping.album import Album

logger = logging.getLogger('database_manager')
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def create_tables():
    engine = create_engine(SQL_URL, echo=True)
    Base.metadata.create_all(engine)


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


def get_label_id(album_label_name, session):
    label = session.query(Label).filter_by(name=album_label_name).first()
    if not label:
        label_to_insert = Label(name=album_label_name)
        session.add(label_to_insert)
    return session.query(Label).filter_by(name=album_label_name).first().id


def get_artist_id(album_artist_name, session):
    artist = session.query(Artist).filter_by(name=album_artist_name).first()
    if artist:
        return artist.id

    artist_to_insert = Artist(name=album_artist_name)
    session.add(artist_to_insert)
    # retrieve id from add
    return session.query(Artist).filter_by(name=album_artist_name).first().id


def insert(albums: List[Album]):
    session = sql_session()
    album_models = []
    for album in albums:
        artist = Artist(name=album.artist.name)
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
