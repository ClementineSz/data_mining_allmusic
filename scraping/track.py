from datetime import datetime, timedelta

from scraping.artist import Artist
from scraping.config import HtmlTags, HtmlClasses
from scraping.utils import protected_from_attribute_error, to_title, strip


class Track:
    def __init__(self, soup):
        self.soup = soup
        self._composers = []
        composers_string = self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.COMPOSER}).text
        if composers_string.strip():
            for composer_name in composers_string.split('/'):
                self._composers.append(Artist(composer_name))

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def title(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.TITLE}).text

    @property
    @protected_from_attribute_error
    def composers(self):
        return self._composers

    @property
    @protected_from_attribute_error
    def duration(self):
        try:
            time_string = self.soup.find(HtmlTags.TD, {'class': HtmlClasses.TIME}).text.strip()
            time = datetime.strptime(time_string, '%M:%S')
            return timedelta(seconds=time.second, minutes=time.minute).seconds
        except ValueError:
            pass
