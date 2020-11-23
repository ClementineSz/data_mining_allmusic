import re

from scraping.config import DATA_CLASS, PROFILE_USER_RATING_CLASS, MIDDLE_CLASS


class AlbumReview:
    def __init__(self, soup):
        self.soup = soup

    @property
    def name(self):
        return self.soup.find('div', {"class": DATA_CLASS}).find_all('p')[0].text.strip()

    @property
    def date(self):
        return self.soup.find('div', {"class": DATA_CLASS}).find_all('p')[1].text.strip()

    @property
    def rating(self):
        classes = self.soup.find('div', {"class": DATA_CLASS}).find('div', {"class": PROFILE_USER_RATING_CLASS})['class']
        rating_class = classes[-1]
        rating = re.search('([0-9])', rating_class).group(1)
        return rating

    @property
    def content(self):
        return self.soup.find('div', {'class': MIDDLE_CLASS}).text.strip()

    def json(self):
        return {
            'name': self.name,
            'date': self.date,
            'rating': self.rating,
            'content': self.content
        }






