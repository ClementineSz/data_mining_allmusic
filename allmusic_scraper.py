from bs4 import BeautifulSoup

import utils
from scraping.album import Album
from scraping.config import BASE_URL, NEW_RELEASES_ENDPOINT


def get_new_albums():
    """

    """
    url = BASE_URL + NEW_RELEASES_ENDPOINT
    response = utils.request(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract all new features from the html
    albums_divs = soup.find_all('div', {"class": "new-release"})

    albums = []
    for i, album_div in enumerate(albums_divs):
        album = Album(album_div)
        utils.pretty_print(album.json())

        print(f'[{i}/{len(albums_divs)}] - Finished extracting {album.title}')

        albums.append(album)
    return albums
