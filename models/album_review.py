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
        return self.soup.find('div', {"class": "data"}).find('div', {"class": "profile-user-rating"})






