import re


class AlbumReview:
    def __init__(self, soup):
        self.soup = soup

    @property
    def name(self):
        return self.soup.find('div', {"class": "data"}).find_all('p')[0].text.strip()

    @property
    def date(self):
        return self.soup.find('div', {"class": "data"}).find_all('p')[1].text.strip()

    @property
    def rating(self):
        classes = self.soup.find('div', {"class": "data"}).find('div', {"class": "profile-user-rating"})['class']
        rating_class = classes[-1]
        rating = re.search('([0-9])', rating_class).group(1)
        return rating

    def json(self):
        return {
            'name': self.name,
            'date': self.date,
            'rating': self.rating,
        }






