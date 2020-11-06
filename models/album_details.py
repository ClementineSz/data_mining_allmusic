from models.album_reviews import AlbumReviews
from models.constants import BASE_URL, NEW_RELEASES, ALBUM, FETCH_REVIEW
from models.soup_loader import SoupLoader


class AlbumDetails(SoupLoader):
    def __init__(self, id, url):
        super().__init__(url=url)
        self.id = id

    @property
    def duration(self):
        try:
            return self.find('div', {"class": "duration"}).span.text.strip()
        except AttributeError:
            pass

    @property
    def genre(self):
        return self.find('div', {"class": "genre"}).a.text.strip()

    @property
    def genre(self):
        return self.find('div', {"class": "genre"}).a.text.strip()

    @property
    def review_url(self):
        #return self.find('li', {"class": "user_reviews"}).a['href'].strip()
        return ALBUM + FETCH_REVIEW + self.id

    @property
    def reviews(self):
        return AlbumReviews(self.review_url)
