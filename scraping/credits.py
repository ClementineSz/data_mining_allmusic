from bs4 import BeautifulSoup

from scraping import utils
from scraping.config import Endpoints, HtmlClasses, HtmlTags
from scraping.credit import Credit
from scraping.utils import protected_from_attribute_error


class Credits:
    def __init__(self, album):
        self.album = album
        self.soup = self.load_soup()

    def load_soup(self):
        url = utils.create_url(Endpoints.BASE, self.album.details_url, Endpoints.CREDITS)
        response = utils.fetch(url)
        return BeautifulSoup(response.text, 'html.parser')

    @property
    @protected_from_attribute_error
    def credits(self):
        section_credits = self.soup.find(HtmlTags.SECTION, {'class': HtmlClasses.CREDITS})
        credit_tags = section_credits.find_all(HtmlTags.TD, {"class": "artist"})
        credit_tags = [tag.find_parent(HtmlTags.TR) for tag in credit_tags]
        return [Credit(tag) for tag in credit_tags]

    def __iter__(self):
        credits_to_iterate = []
        if self.credits:
            for credit in self.credits:
                credits_to_iterate.append(credit)
        return credits_to_iterate.__iter__()
