from bs4 import BeautifulSoup

import utils
from models.album import Album
from models.constants import BASE_URL, NEW_RELEASES


def get_new_albums():
    """

    """
    url = BASE_URL + NEW_RELEASES
    response = utils.get_request(url)
    soup = BeautifulSoup(response.txt, 'html.parser')

    # Extract all new features from the html
    albums_divs = soup.find_all('div', {"class": "new-release"})

    return [Album(album_div) for album_div in albums_divs]
