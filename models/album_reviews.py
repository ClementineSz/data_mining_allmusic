from models.album_review import AlbumReview
from models.soup_loader import SoupLoader


class AlbumReviews(SoupLoader):
    def __init__(self, url):
        super().__init__(url=url)

    def __getitem__(self, index):
        return self._reviews[index]

    @property
    def _reviews(self):
        reviews_div = self.soup.find_all('div', {"class": "user_review"})
        reviews = [AlbumReview(review_div) for review_div in reviews_div]
        return reviews

