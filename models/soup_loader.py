from bs4 import BeautifulSoup

from models.constants import BASE_URL
from utils import make_request


class SoupLoader:
    def load_soup(self):
        url = BASE_URL + self.url
        response = make_request(url)
        return BeautifulSoup(response.text, 'html.parser')