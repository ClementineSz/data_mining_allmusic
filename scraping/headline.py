from scraping.config import HtmlTags, HtmlClasses
from scraping.utils import protected_from_attribute_error


class Headline:
    def __init__(self, soup):
        self.soup = soup

    @protected_from_attribute_error
    @property
    def author(self):
        """ Extracts author of headline from the html

        @return:
        """
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.AUTHOR}).text.strip('\n -')

    @protected_from_attribute_error
    @property
    def content(self):
        """ Extracts content of headline from the html

        @return:
        """
        return self.soup.find(text=True, recursive=False).strip()
