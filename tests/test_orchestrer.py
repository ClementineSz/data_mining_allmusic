from database.database_manager import insert_albums
from orchester.orchester import apply_middle_mans
from scraping.album import Album
from scraping.scraper import get_albums_html


def test_orchestrer():
    albums_html = get_albums_html()

    albums = [Album(albums_html.pop(0))]
    apply_middle_mans(albums)

    insert_albums(albums)
