import re

from scraping.credits import Credits
from scraping.details import Details
from scraping.config import HtmlTags, HtmlClasses, Patterns
from scraping.headline import Headline

from scraping.utils import protected_from_attribue_error


class Album:
    def __init__(self, soup):
        self.soup = soup
        self.details = Details(self)
        self.credits = Credits(self)

    @property
    @protected_from_attribue_error
    def title(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.TITLE}).text.strip().lower()

    @property
    @protected_from_attribue_error
    def artist(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.ARTIST}).text.strip()

    @property
    @protected_from_attribue_error
    def genre(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.GENRES}).text.strip()

    @property
    @protected_from_attribue_error
    def label(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.LABELS}).text.strip()

    @property
    @protected_from_attribue_error
    def details_url(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.IMAGE}).a['href'].strip()

    @property
    def reference_number(self):
        return re.search(Patterns.REFERENCE_NUMBER, self.details_url).group(1)

    @property
    @protected_from_attribue_error
    def headline_review(self):
        headline_div = self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.HEADLINE_REVIEW})
        return Headline(headline_div)

