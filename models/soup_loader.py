from bs4 import BeautifulSoup

from models.constants import ALBUM, BASE_URL
from utils import get_request


class SoupLoader:
    def __init__(self, soup=None, url=None):
        self.url = url
        self._soup = soup

    @property
    def soup(self):
        if not self._soup:
            self._load_soup()
        return self._soup

    def _load_soup(self):
        url = BASE_URL + self.url
        response = get_request(url)
        self._soup = BeautifulSoup(response.text, 'html.parser')

    def find(self, div, parameters):
        try:
            return self.soup.find(div, parameters).find('span').text.strip()
        except AttributeError:
            print(f'No {parameters} in {div}')
