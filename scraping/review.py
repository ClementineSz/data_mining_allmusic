import re

from scraping.config import HtmlTags, HtmlClasses, Patterns
from scraping.utils import protected_from_attribue_error


class Review:
    def __init__(self, soup):
        self.soup = soup

    @property
    @protected_from_attribue_error
    def name(self):
        return self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.DATA}).find_all(HtmlTags.P)[0].text.strip()

    @property
    @protected_from_attribue_error
    def date(self):
        return self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.DATA}).find_all(HtmlTags.P)[1].text.strip()

    @property
    @protected_from_attribue_error
    def rating(self):
        classes = self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.DATA}).find(HtmlTags.DIV, {"class": HtmlClasses.PROFILE_USER_RATING})['class']
        rating_class = classes[-1]
        rating = re.search(Patterns.REVIEW_RATING, rating_class).group(1)
        return rating

    @property
    @protected_from_attribue_error
    def content(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.MIDDLE}).text.strip()






