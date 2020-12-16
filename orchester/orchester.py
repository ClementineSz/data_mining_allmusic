from config import MIDDLE_MANS
from database import database_manager
from scraping.scraper import get_new_albums


def filter_moods(albums, mood):
    if mood:
        return [album for album in albums if mood.title() in album.details.moods]
    return albums


def orchestrate(mood):
    albums = get_new_albums()
    albums = filter_moods(albums, mood)
    apply_middle_mans(albums)
    database_manager.insert_albums(albums)


def apply_middle_mans(albums):
    for middle_man in MIDDLE_MANS:
        middle_man.handle(albums)
