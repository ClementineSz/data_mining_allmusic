from scraping.config import HtmlTags, HtmlClasses
from scraping.utils import protected_from_attribue_error


class Credit:
    def __init__(self, soup):
        self.soup = soup

    @property
    @protected_from_attribue_error
    def artist(self):
        return self.soup.find(HtmlTags.TD, {'class': HtmlClasses.ARTIST}).a.text.strip()

    @property
    @protected_from_attribue_error
    def role(self):
        return self.soup.find(HtmlTags.TD, {'class': HtmlClasses.CREDIT}).text.strip()