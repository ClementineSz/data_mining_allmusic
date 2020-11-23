import json
import re

from scraping.album_credits import AlbumCredits
from scraping.album_details import AlbumDetails
from scraping.config import ALBUM_ENDPOINT
from utils import soup_extractor



class Album:
    def __init__(self, soup):
        self.soup = soup
        self.details = AlbumDetails(self)
        self.credits = AlbumCredits(self)

    @property
    @soup_extractor
    def title(self):
        return self.soup.find('div', {"class": TITLE}).text.strip().lower()

    @property
    @soup_extractor
    def artist(self):
        return self.soup.find('div', {"class": ARTIST}).text.strip()

    @property
    @soup_extractor
    def genre(self):
        return self.soup.find('div', {"class": GENRES}).text.strip()

    @property
    @soup_extractor
    def label(self):
        return self.soup.find('div', {"class": LABELS}).text.strip()

    @property
    @soup_extractor
    def details_url(self):
        return self.soup.find('div', {"class": IMAGE_CONTAINER}).a['href'].strip()


    @property
    def id(self):
        return re.search('.*-(.*)', self.details_url).group(1)

    @property
    @soup_extractor
    def headline_review(self):
        headline_div = self.soup.find('div', {"class": HEADLINE_REVIEW})
        return {
            'author': headline_div.find('div', {"class": AUTHOR}).text.strip('\n -'),
            'content': headline_div.find(text=True, recursive=False).strip(),
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
            'headline_review': self.headline_review,
            'credits': self.credits.json()
        }


