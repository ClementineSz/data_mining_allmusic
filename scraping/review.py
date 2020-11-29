import re
from dateutil.parser import parse

from scraping.config import HtmlTags, HtmlClasses, Patterns
from scraping.utils import protected_from_attribute_error


class Review:
    def __init__(self, soup):
        self.soup = soup

    @property
    @protected_from_attribute_error
    def author(self):
        """ Extracts author from the html
        @return:
        """
        return self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.DATA}).find_all(HtmlTags.P)[0].text.strip()

    @property
    @protected_from_attribute_error
    def date(self):
        """ Extracts date from the html
        @return:
        """
        string_date = self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.DATA}).find_all(HtmlTags.P)[1].text.strip()
        return parse(string_date)

    @property
    @protected_from_attribute_error
    def rating(self):
        """ Extracts rating from the html
        @return:
        """
        classes = self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.DATA}).find(HtmlTags.DIV, {"class": HtmlClasses.PROFILE_USER_RATING})['class']
        rating_class = classes[-1]
        rating = re.search(Patterns.REVIEW_RATING, rating_class).group(1)
        return rating

    @property
    @protected_from_attribute_error
    def content(self):
        """ Extracts content from the html
        @return:
        """
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.MIDDLE}).text.strip()






