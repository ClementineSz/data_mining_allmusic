from database.database_manager import insert_albums, refresh_tables
from orchestration.orchester import apply_middle_mans
from scraping.album import Album
from scraping.scraper import get_albums_html


def test_orchestrer():
    albums_html = get_albums_html()

    albums = [Album(albums_html.pop(0))]
    apply_middle_mans(albums)

    insert_albums(albums)


def test_one_album():
    refresh_tables()
    url = 'mw0003434729'
    albums_html = get_albums_html()

    albums = [Album(html) for html in albums_html]
    albums = [album for album in albums if album.reference_number == url]
    apply_middle_mans(albums)

    insert_albums(albums)
