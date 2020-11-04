from models.soup_loader import SoupLoader


class AlbumDetails(SoupLoader):
    def __init__(self, url):
        super().__init__(url=url)


    @property
    def duration(self):
        return self.find('div', {"class": "duration"})
