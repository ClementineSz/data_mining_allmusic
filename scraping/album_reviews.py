from bs4 import BeautifulSoup

from scraping.album_review import AlbumReview
from scraping.config import BASE_URL, USER_REVIEWS_ENDPOINT
from utils import request


class AlbumReviews:
    def __init__(self, details):
        self.details = details
        self.soup = self.load_soup()

    def load_soup(self):
        url = BASE_URL + self.details.review_url
        data = {
            'title': self.details.album.title
        }
        headers = {
            'referer': BASE_URL + self.details.album.details_url + USER_REVIEWS_ENDPOINT
        }
        response = request(url, headers=headers, data=data, post=True)
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

