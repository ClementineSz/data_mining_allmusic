from database.database_manager import sql_session, create_tables, drop_tables, get_or_create, create_database, \
    insert_album
from models.album import Album as ModelAlbum, Artist, Label, Mood, Theme, Style, Track, ReviewBody, Genre, Review, \
    Credit, Role
from scraping.album import Album as ScrapingAlbum
from scraping.scraper import get_albums_html, get_new_albums


def test_insert_all():
    session = sql_session()

    albums_html = get_albums_html()

    for album_html in albums_html:
        album = ScrapingAlbum(album_html)
        insert_album(session, album)

def test_insert_one():
    session = sql_session()

    albums_html = get_albums_html()

    album = ScrapingAlbum(albums_html.pop(0))
    insert_album(session, album)

def test_scrape_all_data():
    get_new_albums()


def test_create_tables():
    create_tables()


def test_drop_tables():
    drop_tables()


def test_refresh_tables():
    drop_tables()
    create_tables()


def test_refresh_and_insert():
    drop_tables()
    create_tables()
    test_insert_all()


def test_create_database():
    create_database()
