import re

from scraping.artist import Artist
from scraping.config import HtmlTags, HtmlClasses, Patterns
from scraping.credits import Credits
from scraping.details import Details
from scraping.headline import Headline
from scraping.utils import protected_from_attribute_error, to_title, strip


class Album:
    def __init__(self, soup):

        self.soup = soup
        self.details = Details(self)
        self.credits = Credits(self)
        self._popularity = None
        self._artists = []
        artists_string = self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.ARTIST}).text
        if artists_string.strip():
            for artist_name in artists_string.split('/'):
                self._artists.append(Artist(artist_name))

    @property
    def popularity(self):
        return self._popularity

    @popularity.setter
    def popularity(self, value):
        self._popularity = value

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def title(self):
        """ Get the title of an album

        @return: title of an album
        """
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.TITLE}).text.strip().lower()

    @property
    @protected_from_attribute_error
    def artists(self):
        """ Extract artist names from the soup

        @return:  list of artists
        """

        return self._artists

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def label(self):
        """ Extract label names from the soup

        @return: list of labels
        """
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.LABELS}).text.strip()

    @property
    @protected_from_attribute_error
    def details_url(self):
        """ Extract details url from the soup

        @return: list of labels
        """
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.IMAGE}).a['href'].strip()

    @property
    def reference_number(self):
        """ Get the reference number of an album

        @return: reference number
        """
        return re.search(Patterns.REFERENCE_NUMBER, self.details_url).group(1)

    @property
    @protected_from_attribute_error
    def headline_review(self):
        """ Get the headline review of an album

        @return: headline review
        """
        headline_div = self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.HEADLINE_REVIEW})
        return Headline(headline_div)
