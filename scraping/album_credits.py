from bs4 import BeautifulSoup

from request_manager import request_manager
from request_manager.request_manager import fetch
from scraping.config import Endpoints, HtmlClasses, HtmlTags
from scraping.utils import protected_from_attribue_error


class AlbumCredits:
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
        section_credits_tr = section_credits.find_all(HtmlTags.TR)
        credits_list = []
        for tr in section_credits_tr:
            artist = tr.find(HtmlTags.TD, {'class': HtmlClasses.ARTIST}).a.text.strip()
            role = tr.find(HtmlTags.TD, {'class': HtmlClasses.CREDIT}).text.strip()
            credit = {
                'artist': artist,
                'role': role
            }
            credits_list.append(credit)
        return credits_list

    def json(self):
        return self.credits
