import logging
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.config import SQL_URL, DB_NAME
from models.album import Album as ModelAlbum
from models.album import Artist, Label, Style, Mood, Theme, Track, ReviewBody, Base, Genre, Review, Credit, Role
from scraping.album import Album

logger = logging.getLogger('main')


def get(session, model, **kwargs):
    return session.query(model).filter_by(**kwargs).first()


def create(session, obj):
    session.add(obj)
    session.commit()


def get_or_create(session, model, **kwargs):
    """
    Check if the instance exists in the database and if not, creates it

    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def handle_album_artists(session, model_album, album):
    if not album.artists:
        return
    artists = []
    for artist in album.artists:
        model_artist = get_or_create(session, Artist, name=artist.name)
        model_artist.popularity = artist.popularity
        model_artist.followers = artist.followers
        artists.append(model_artist)
    model_album.artists = artists


def insert_album(session, album):
    """ Inserts an album on the database

    @param session:
    @param album:
    """
    label = get_or_create(session, Label, name=album.label)
    genre = get_or_create(session, Genre, description=album.details.genre)
    review_body = get_or_create(session, ReviewBody, content=album.details.review_body)
    model_album = get_or_create(session, ModelAlbum, reference_number=album.reference_number)

    model_album.label = label
    model_album.genre = genre
    model_album.title = album.title
    model_album.review_body = review_body
    # model_album.headline_review_author = album.headline_review.author
    # model_album.headline_review_content = album.headline_review.content
    model_album.popularity = album.popularity

    handle_album_artists(session, model_album, album)
    handle_album_credits(album, model_album, session)
    handle_album_moods(album, model_album, session)
    handle_album_styles(album, model_album, session)
    handle_album_themes(album, model_album, session)
    handle_album_reviews(album, model_album, session)
    handle_album_tracks(album, model_album, session)

    session.add(model_album)
    session.commit()
    logger.info(f'Added {album.title} to the database.')


def handle_album_tracks(album, model_album, session):
    if not album.details.tracks:
        return
    tracks = []
    for track in album.details.tracks:
        model_track = get_or_create(session, Track, title=track.title)
        composers = []
        for composer in track.composers:
            model_artist = get_or_create(session, Artist, name=composer.name)
            model_artist.popularity = composer.popularity
            model_artist.followers = composer.followers
            composers.append(model_artist)
        model_track.duration = track.duration
        model_track.composers = composers
        tracks.append(model_track)
    model_album.tracks = tracks


def handle_album_reviews(album, model_album, session):
    if album.details.reviews:
        reviews = [get_or_create(session, Review, content=review.content, author=review.author, date=review.date) for
                   review
                   in
                   album.details.reviews]
        model_album.reviews = reviews


def handle_album_themes(album, model_album, session):
    if album.details.themes:
        themes = [get_or_create(session, Theme, description=theme) for theme in album.details.themes]
        model_album.themes = themes


def handle_album_styles(album, model_album, session):
    if album.details.styles:
        styles = [get_or_create(session, Style, description=style) for style in album.details.styles]
        model_album.styles = styles


def handle_album_moods(album, model_album, session):
    if album.details.moods:
        moods = [get_or_create(session, Mood, description=mood) for mood in album.details.moods]
        model_album.moods = moods


def handle_album_credits(album, model_album, session):
    if not album.credits:
        return

    credits = []
    for credit in album.credits:
        for role in credit.roles:
            model_artist = get_or_create(session, Artist, name=credit.artist.name)
            model_artist.popularity = credit.artist.popularity
            model_artist.followers = credit.artist.followers
            role = get_or_create(session, Role, name=role)
            credit = get_or_create(session, Credit, artist=model_artist, role=role)

            credits.append(credit)
    model_album.credits = credits


def create_database():
    """ Create a database

    """
    engine = create_engine(SQL_URL, echo=False)
    engine.execute(f"CREATE DATABASE {DB_NAME}")
    engine.execute(f"SET collation_connection = 'utf8_general_ci';")
    engine.execute(f"ALTER DATABASE {DB_NAME} CHARACTER SET utf8 COLLATE utf8_general_ci;")


def drop_database():
    """ Drop the database

    """
    engine = create_engine(SQL_URL + DB_NAME, echo=False)
    engine.execute(f"DROP DATABASE {DB_NAME}")


def refresh_tables():
    drop_tables()
    create_tables()


def create_tables():
    """ Create the tables in the database

    """
    engine = create_engine(SQL_URL + DB_NAME, echo=False)
    Base.metadata.create_all(engine)
    engine.execute(f"ALTER TABLE review_body CONVERT TO CHARACTER SET utf8;")


def drop_tables():
    """ Drop the tables in the  database

    """
    engine = create_engine(SQL_URL + DB_NAME, echo=False)
    Base.metadata.drop_all(engine)


def sql_session():
    """ Create a session

    @return:
    """
    engine = create_engine(SQL_URL + DB_NAME, echo=False)
    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()


def insert_albums(albums: List[Album]):
    """ Insert albums in the database

    @param albums:
    """
    session = sql_session()
    for i, album in enumerate(albums):
        logger.info(f"{i}/{len(albums)} - {album.title}")
        insert_album(session, album)
