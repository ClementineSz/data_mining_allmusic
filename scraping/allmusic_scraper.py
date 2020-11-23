from bs4 import BeautifulSoup

import utils
from request_manager import request_manager
from scraping.album import Album
from scraping.config import Endpoints, HtmlClasses


def get_new_albums():
    """

    """
    url = request_manager.create_url(Endpoints.BASE, Endpoints.NEW_RELEASES)
    response = request_manager.fetch(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract all new features from the html
    albums_divs = soup.find_all('div', {"class": HtmlClasses.NEW_RELEASE})

    albums = []
    for i, album_div in enumerate(albums_divs):
        album = Album(album_div)
        utils.pretty_print(album.json())

        print(f'[{i}/{len(albums_divs)}] - Finished extracting {album.title}')

        albums.append(album)
    return albums
