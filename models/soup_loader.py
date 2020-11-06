from bs4 import BeautifulSoup

from models.constants import BASE_URL
from utils import make_request


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
        response = make_request(url)
        self._soup = BeautifulSoup(response.text, 'html.parser')

    def find(self, div, parameters):
        try:
            return self.soup.find(div, parameters)
        except AttributeError:
            print(f'No {parameters} in {div}')
