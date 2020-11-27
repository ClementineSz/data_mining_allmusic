from scraping.config import HtmlTags, HtmlClasses
from scraping.utils import protected_from_attribue_error, to_title, strip


class Credit:
    def __init__(self, soup):
        self.soup = soup

    @property
    @protected_from_attribue_error
    @to_title
    @strip
    def artist_name(self):
        return self.soup.find(HtmlTags.TD, {'class': HtmlClasses.ARTISTS}).a.text

    @property
    @protected_from_attribue_error
    @to_title
    @strip
    def roles(self):
        return [role.strip().lower() for role in self.soup.find(HtmlTags.TD, {'class': HtmlClasses.CREDIT}).text.split(',')]


    @property
    @protected_from_attribue_error
    @to_title
    @strip
    def composer(self):
        return self.soup.find(HtmlTags.TD, {'class': HtmlClasses.COMPOSER}).text

