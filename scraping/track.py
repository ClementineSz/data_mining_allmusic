from datetime import datetime, timedelta

from scraping.config import HtmlTags, HtmlClasses
from scraping.utils import protected_from_attribue_error


class Track:
    def __init__(self, soup):
        self.soup = soup

    @property
    @protected_from_attribue_error
    def title(self):
        return self.soup.find(HtmlTags.TD, {'class': HtmlClasses.TRACKNUM}).text.strip()

    @property
    @protected_from_attribue_error
    def composer(self):
        return self.soup.find(HtmlTags.TD, {'class': HtmlClasses.COMPOSER}).text.strip()

    @property
    @protected_from_attribue_error
    def performer(self):
        return self.soup.find(HtmlTags.TD, {'class': HtmlClasses.PERFORMER}).text.strip()

    @property
    @protected_from_attribue_error
    def duration(self):
        try:
            time_string = self.soup.find(HtmlTags.TD, {'class': HtmlClasses.TIME}).text.strip()
            time = datetime.strptime(time_string, '%M:%S')
            return timedelta(seconds=time.second, minutes=time.minute).seconds
        except ValueError:
            pass
