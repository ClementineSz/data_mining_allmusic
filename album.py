class Album:
    def __init__(self, soup):
        self.soup = soup

    @property
    def name(self):
        return self.soup.find('div', {"class": "title"}).text.strip()

    def artist(self):
        return self.soup.find('div', {"class": "artist"}).text.strip()

    def genre(self):
        return self.soup.find('div', {"class": "genres"}).text.strip()

    def label(self):
        return self.soup.find('div', {"class": "labels"}).text.strip()

    def url(self):
        return self.soup.find('div', {"class": "image-container"}).a['href'].strip()


