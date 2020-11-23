from bs4 import BeautifulSoup

from request_manager import request_manager
from request_manager.request_manager import fetch
from scraping.album_review import AlbumReview
from scraping.config import Endpoints, HtmlTags, HtmlClasses
from scraping.utils import protected_from_attribue_error


class AlbumReviews:
    def __init__(self, details):
        self.details = details
        self.soup = self.load_soup()

    def load_soup(self):
        data = {'title': self.details.album.title}
        headers = {'referer': Endpoints.BASE + self.details.album.details_url + Endpoints.USER_REVIEWS}
        url = request_manager.get_formatted_url(Endpoints.BASE, self.details.review_url)

        response = request_manager.fetch(url, headers=headers, data=data, post=True)

        return BeautifulSoup(response.text, 'html.parser')

    def __getitem__(self, index):
        return self.reviews[index]

    @property
    @protected_from_attribue_error
    def reviews(self):
        reviews_div = self.soup.find_all(HtmlTags.DIV, {"class": HtmlClasses.USER_REVIEW})
        reviews = [AlbumReview(review_div) for review_div in reviews_div]
        return reviews

    def json(self):
        return [review.json() for review in self.reviews]

