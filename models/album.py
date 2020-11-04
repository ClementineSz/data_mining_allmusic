from models.album_details import AlbumDetails
from models.soup_loader import SoupLoader

IMAGE_CONTAINER = "image-container"

LABELS = "labels"

GENRES = "genres"

ARTIST = "artist"

TITLE = "title"


class Album(SoupLoader):
    def __init__(self, soup):
        super().__init__(soup=soup, loaded=True)

    @property
    def name(self):
        return self.find('div', {"class": TITLE}).text.strip()

    @property
    def artist(self):
        return self.find('div', {"class": ARTIST}).text.strip()

    @property
    def genre(self):
        return self.find('div', {"class": GENRES}).text.strip()

    @property
    def label(self):
        return self.find('div', {"class": LABELS}).text.strip()

    @property
    def details_url(self):
        return self.find('div', {"class": IMAGE_CONTAINER}).a['href'].strip()

    @property
    def details(self):
        return AlbumDetails(url=self.details_url)


