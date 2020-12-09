import logging
import sys

from bs4 import BeautifulSoup

from scraping import utils
from scraping.album import Album
from scraping.config import Endpoints, HtmlClasses, HtmlTags

logger = logging.getLogger('main.scraper')

def get_new_albums():
    """  Create album per new feature

    @return: a list of albums
    """
    albums_divs = get_albums_html()

    albums = []
    for i, album_div in enumerate(albums_divs):
        album = Album(album_div)

        logger.info(f'[{i}/{len(albums_divs)}] - Finished extracting {album.title}')

        albums.append(album)
    return albums


def get_albums_html():
    """ Get the html of new release page and find the divs with new release information

    @return: all divs with information of new feature album
    """
    url = utils.create_url(Endpoints.BASE, Endpoints.NEW_RELEASES)
    response = utils.fetch(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    albums_divs = soup.find_all(HtmlTags.DIV, {"class": HtmlClasses.NEW_RELEASE})
    return albums_divs
