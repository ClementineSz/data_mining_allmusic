import logging
import sys
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.config import SQL_URL, DB_NAME
from models.album import Album, Artist, Label, Style, Mood, Theme, Track, ReviewBody, Base, Genre, Review, Credit, Role
from scraping.album import Album

from models.album import Album as ModelAlbum

logger = logging.getLogger('database_manager')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def get_or_create(session: object, model: object, kwargs: object) -> object:
    """ Check if the instance exists in the database and if not, creates it

    @param session:
    @param model:
    @param kwargs:
    @return:
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def insert_album(session, album):
    """ Inserts an album on the database

    @param session:
    @param album:
    """
    label = get_or_create(session, Label, name=album.label)
    genre = get_or_create(session, Genre, description=album.details.genre)
    review_body = get_or_create(session, ReviewBody, content=album.details.review_body)

    model_album = get_or_create(session, ModelAlbum, reference_number=album.reference_number)

    model_album.review_body = review_body
    model_album.title = album.title
    model_album.label = label
    model_album.headline_review_author = album.headline_review.author
    model_album.headline_review_content = album.headline_review.content

    if album.artists:
        artists = [get_or_create(session, Artist, name=artist) for artist in album.artists]
        model_album.artists = artists

    if album.credits:
        credits = []
        for credit in album.credits:
            for role in credit.roles:
                credits.append(
                    get_or_create(session, Credit, artist=get_or_create(session, Artist, name=credit.artist_name),
                                  role=get_or_create(session, Role, name=role)))
        model_album.credits = credits

    if album.details.moods:
        moods = [get_or_create(session, Mood, description=mood) for mood in album.details.moods]
        model_album.moods = moods

    if album.details.styles:
        styles = [get_or_create(session, Style, description=style) for style in album.details.styles]
        model_album.styles = styles

    if album.details.themes:
        themes = [get_or_create(session, Theme, description=theme) for theme in album.details.themes]
        model_album.themes = themes

    model_album.genre = genre
    if album.details.reviews:
        reviews = [get_or_create(session, Review, content=review.content, author=review.author, date=review.date) for
                   review
                   in
                   album.details.reviews]
        model_album.reviews = reviews

    if album.details.tracks:
        tracks = []
        for track in album.details.tracks:
            track_model = get_or_create(session, Track, title=track.title)
            composers = [get_or_create(session, Artist, name=composer) for composer in track.composers]
            track_model.duration = track.duration
            track_model.composers = composers
            tracks.append(track_model)
        model_album.tracks = tracks

    session.add(model_album)
    session.commit()
    logger.info(f'Added {album.title} to the database.')


def create_database():
    """ Create a database

    """
    engine = create_engine(SQL_URL, echo=True)
    engine.execute(f"CREATE DATABASE {DB_NAME}")


def drop_database():
    """ Drop the database

    """
    engine = create_engine(SQL_URL + DB_NAME, echo=True)
    engine.execute(f"DROP DATABASE {DB_NAME}")


def create_tables():
    """ Create the tables in the database

    """
    engine = create_engine(SQL_URL + DB_NAME, echo=True)
    Base.metadata.create_all(engine)


def drop_tables():
    """ Drop the tables in the  database

    """
    engine = create_engine(SQL_URL + DB_NAME, echo=True)
    Base.metadata.drop_all(engine)


def sql_session():
    """ Create a session

    @return:
    """
    engine = create_engine(SQL_URL + DB_NAME, echo=True)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


def insert_albums(albums: List[Album]):
    """ Insert albums in the database

    @param albums:
    """
    session = sql_session()
    for album in albums:
        insert_album(session, album)
