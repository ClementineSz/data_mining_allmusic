from bs4 import BeautifulSoup

from models.album_review import AlbumReview
from models.constants import BASE_URL, USER_REVIEWS
from models.soup_loader import SoupLoader
from models.soup_manager import SoupManager
from utils import make_request


class AlbumReviews(SoupLoader):
    def __init__(self, details):
        self.details = details
        super().__init__(self.details.album.details_url)

    def load_soup(self):
        url = BASE_URL + self.details.review_url
        data = {
            'title': self.details.album.title
        }
        headers = {
            'referer': BASE_URL + self.details.album.details_url + USER_REVIEWS
        }
        response = make_request(url, headers=headers, data=data, post=True)
        return BeautifulSoup(response.text, 'html.parser')

    def __getitem__(self, index):
        return self.reviews[index]

    @property
    def reviews(self):
        reviews_div = self.soup.find_all('div', {"class": "user_review"})
        reviews = [AlbumReview(review_div) for review_div in reviews_div]
        return reviews

    def json(self):
        return [review.json() for review in self.reviews]

