from scraping.config import HtmlTags, HtmlClasses
from scraping.utils import protected_from_attribute_error, to_title, strip


class Credit:
    def __init__(self, soup):
        self.soup = soup

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def artist_name(self):
        """ Get artist name in credits parts of an album

        @return:
        """
        return self.soup.find(HtmlTags.TD, {'class': HtmlClasses.ARTISTS}).a.text

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def roles(self):
        """ Get all the roles of an artist in the credits part

        @return: role of an artist on the production of an album
        """
        return [role.strip().lower() for role in
                self.soup.find(HtmlTags.TD, {'class': HtmlClasses.CREDIT}).text.split(',')]

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def composer(self):
        """ Get the composer of an album

        @return: composer of an album
        """
        return self.soup.find(HtmlTags.TD, {'class': HtmlClasses.COMPOSER}).text
