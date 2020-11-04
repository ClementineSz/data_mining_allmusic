class Album:
    def __init__(self, soup):
        self.soup = soup

    @property
    def artist(self):
        return self.soup.find('div', {"class": "artist"}).text.strip()