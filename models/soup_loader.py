from bs4 import BeautifulSoup

from models.constants import BASE_URL
from utils import make_request


class SoupLoader:
    def __init__(self, url):
        self.url = url
        self.soup = self.load_soup()

    def load_soup(self):
        url = BASE_URL + self.url
        response = make_request(url)
        return BeautifulSoup(response.text, 'html.parser')