import json
import re
import string

from models.album_details import AlbumDetails
from models.constants import ALBUM
from models.soup_manager import SoupManager

AUTHOR = "author"

HEADLINE_REVIEW = "headline-review"

IMAGE_CONTAINER = "image-container"
LABELS = "labels"
GENRES = "genres"
ARTIST = "artist"
TITLE = "title"


class Album:
    def __init__(self, soup):
        self.soup = soup
        self.details = AlbumDetails(self)

    @property
    def title(self):
        return self.soup.find('div', {"class": TITLE}).text.strip().lower()

    @property
    def artist(self):
        return self.soup.find('div', {"class": ARTIST}).text.strip()

    @property
    def genre(self):
        return self.soup.find('div', {"class": GENRES}).text.strip()

    @property
    def label(self):
        return self.soup.find('div', {"class": LABELS}).text.strip()

    @property
    def details_url(self):
        joined_title = '-'.join(self.title.split())
        return f"{ALBUM}{joined_title}-{self.id}"

    @property
    def id(self):
        endpoint = self.soup.find('div', {"class": IMAGE_CONTAINER}).a['href'].strip()
        return re.search('(mw.*)', endpoint).group(1)

    @property
    def headline_review(self):
        headline_div = self.soup.find('div', {"class": HEADLINE_REVIEW})
        return {'author': headline_div.find('div', {"class": AUTHOR}).text.strip(string.punctuation),
                'content': headline_div.text.strip(),
                }

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'genre': self.genre,
            'label': self.label,
            'details_url': self.details_url,
            'details': self.details.json(),
            'headline_review': self.headline_review
        }


