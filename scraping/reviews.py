from bs4 import BeautifulSoup

from request_manager import request_manager
from request_manager.request_manager import fetch
from scraping.review import Review
from scraping.config import Endpoints, HtmlTags, HtmlClasses
from scraping.utils import protected_from_attribue_error


class Reviews:
    def __init__(self, details):
        self.details = details
        self.soup = self.load_soup()

    def load_soup(self):
        data = {'title': self.details.album.title}
        headers = {'referer': request_manager.create_url(Endpoints.BASE, self.details.album.details_url, Endpoints.USER_REVIEWS)}
        url = request_manager.create_url(Endpoints.BASE, self.details.review_url)

        response = request_manager.fetch(url, headers=headers, data=data, post=True)

        return BeautifulSoup(response.text, 'html.parser')

    def __getitem__(self, index):
        return self.reviews[index]

    @property
    @protected_from_attribue_error
    def reviews(self):
        reviews_div = self.soup.find_all(HtmlTags.DIV, {"class": HtmlClasses.USER_REVIEW})
        reviews = [Review(review_div) for review_div in reviews_div]
        return reviews

    def __iter__(self):
        return self.reviews.__iter__()

