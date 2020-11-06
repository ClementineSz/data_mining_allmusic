from models.album_reviews import AlbumReviews
from models.constants import BASE_URL, NEW_RELEASES, ALBUM, FETCH_REVIEW
from models.soup_loader import SoupLoader
from models.soup_manager import SoupManager


class AlbumDetails(SoupLoader):
    def __init__(self, album):
        self.album = album
        super().__init__(self.album.details_url)

        self.reviews = AlbumReviews(self)

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

    def json(self):
        return {
            'duration': self.duration,
            'genre': self.genre,
            'review_url': self.review_url,
            'reviews': self.reviews.json()
        }
