import logging
import sys

from bs4 import BeautifulSoup

import utils
from request_manager import request_manager
from scraping.album import Album
from scraping.config import Endpoints, HtmlClasses, HtmlTags

logger = logging.getLogger('scraper')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def get_new_albums():
    """

    """
    albums_divs = get_albums_html()

    albums = []
    for i, album_div in enumerate(albums_divs):
        album = Album(album_div)

        logger.info(f'[{i}/{len(albums_divs)}] - Finished extracting {album.title}')

        albums.append(album)
    return albums


def get_albums_html():
    url = request_manager.create_url(Endpoints.BASE, Endpoints.NEW_RELEASES)
    response = request_manager.fetch(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    albums_divs = soup.find_all(HtmlTags.DIV, {"class": HtmlClasses.NEW_RELEASE})
    return albums_divs
