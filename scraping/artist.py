from scraping.utils import strip, to_title


class Artist:
    def __init__(self, name) -> None:
        self._name = name
        self._popularity = None
        self._followers = None

    @property
    def followers(self):
        return self._followers

    @followers.setter
    def followers(self, value):
        self._followers = value

    @property
    def popularity(self):
        return self._popularity

    @popularity.setter
    def popularity(self, value):
        self._popularity = value

    @property
    @strip
    @to_title
    def name(self):
        return self._name
