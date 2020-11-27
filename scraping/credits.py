from bs4 import BeautifulSoup

from request_manager import request_manager
from request_manager.request_manager import fetch
from scraping.config import Endpoints, HtmlClasses, HtmlTags
from scraping.credit import Credit
from scraping.utils import protected_from_attribue_error


class Credits:
    def __init__(self, album):
        self.album = album
        self.soup = self.load_soup()

    def load_soup(self):
        url = request_manager.create_url(Endpoints.BASE, self.album.details_url, Endpoints.CREDITS)
        response = fetch(url)
        return BeautifulSoup(response.text, 'html.parser')

    @property
    @protected_from_attribue_error
    def credits(self):
        section_credits = self.soup.find(HtmlTags.SECTION, {'class': HtmlClasses.CREDITS})
        credits_tags = section_credits.find_all(HtmlTags.TR)
        credits_list = [Credit(credit_dit) for credit_dit in credits_tags]
        return credits_list

    def __iter__(self):
        credits_to_iterate = []
        if self.credits:
            for credit in self.credits:
                credits_to_iterate.append(credit)
        return credits_to_iterate.__iter__()
