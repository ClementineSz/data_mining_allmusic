from bs4 import BeautifulSoup

from models.album_review import AlbumReview
from models.constants import BASE_URL
from models.soup_loader import SoupLoader
from utils import make_request


class AlbumReviews(SoupLoader):
    def __init__(self, metadata, url):
        super().__init__(url=url)
        self.metadata = metadata

    def _load_soup(self):
        url = BASE_URL + self.url
        data = {
            'title': self.metadata.get('title')
        }
        response = make_request(url, post=True, data=data)
        self._soup = BeautifulSoup(response.text, 'html.parser')

    def __getitem__(self, index):
        return self._reviews[index]

    @property
    def _reviews(self):
        reviews_div = self.soup.find_all('div', {"class": "user_review"})
        reviews = [AlbumReview(review_div) for review_div in reviews_div]
        return reviews

