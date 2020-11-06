import re

from bs4 import BeautifulSoup

from models.album_details import AlbumDetails
from models.constants import BASE_URL
from models.soup_loader import SoupLoader
from utils import make_request

IMAGE_CONTAINER = "image-container"

LABELS = "labels"

GENRES = "genres"

ARTIST = "artist"

TITLE = "title"


class Album(SoupLoader):
    def __init__(self, soup):
        super().__init__(soup=soup)

    @property
    def title(self):
        return self.find('div', {"class": TITLE}).text.strip()

    @property
    def artist(self):
        return self.find('div', {"class": ARTIST}).text.strip()

    @property
    def genre(self):
        return self.find('div', {"class": GENRES}).text.strip()

    @property
    def label(self):
        return self.find('div', {"class": LABELS}).text.strip()

    @property
    def details_url(self):
        return self.find('div', {"class": IMAGE_CONTAINER}).a['href'].strip()

    @property
    def details(self):
        metadata = {
            'id': self.id,
            'title': self.title,
            'details_url': self.details_url
        }
        return AlbumDetails(metadata)

    @property
    def id(self):
        return re.search('(-)(.*)', self.details_url).group(2)


