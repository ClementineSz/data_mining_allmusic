from bs4 import BeautifulSoup
import re
from models.album_reviews import AlbumReviews
from models.constants import BASE_URL, NEW_RELEASES, ALBUM, FETCH_REVIEW
from utils import make_request

USER_RATING_COUNT = "average-user-rating-count"

RATINGS = "ratings"


class AlbumDetails:
    def __init__(self, album):
        self.album = album
        self.reviews = AlbumReviews(self)
        self.soup = self.load_soup()

    def load_soup(self):
        url = BASE_URL + self.album.details_url
        response = make_request(url)
        return BeautifulSoup(response.text, 'html.parser')

    @property
    def duration(self):
        try:
            return self.soup.find('div', {"class": "duration"}).span.text.strip()
        except AttributeError:
            pass

    @property
    def genre(self):
        return self.soup.find('div', {"class": "genre"}).a.text.strip()

    @property
    def review_url(self):
        return ALBUM + FETCH_REVIEW + self.album.id

    @property
    def user_ratings(self):
        user_ratings_div = self.soup.find('ul', {"class": RATINGS})
        classes = self.soup.find('ul', {"class": "ratings"}).find('div', {"class": "average-user-rating"})['class']
        #rating_class = classes[-1]
        return {
            'number': user_ratings_div.find('span', {"class": USER_RATING_COUNT}).contents[0],
            #'ratings' : re.search('([0-9])', rating_class).group(1)
        }

    def json(self):
        return {
            'duration': self.duration,
            'genre': self.genre,
            'review_url': self.review_url,
            'reviews': self.reviews.json(),
            'user_ratings': self.user_ratings
        }
