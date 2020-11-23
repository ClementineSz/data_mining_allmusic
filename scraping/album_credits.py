from bs4 import BeautifulSoup

from scraping.config import BASE_URL, ALBUM_ENDPOINT, CREDITS_ENDPOINT, CREDITS_CLASS
from utils import request



class AlbumCredits:
    def __init__(self, album):
        self.album = album
        self.soup = self.load_soup()

    def load_soup(self):
        url = BASE_URL + self.album.details_url + CREDITS_ENDPOINT
        print(url)
        response = request(url)
        return BeautifulSoup(response.text, 'html.parser')

    @property
    def credits(self):
        section_credits = self.soup.find('section', {"class": CREDITS_CLASS})
        section_credits_tr = section_credits.find_all('tr')
        credits_list = []
        for tr in section_credits_tr:
            artist = tr.find('td', {"class": "artist"}).a.text.strip()
            role = tr.find('td', {"class": "credit"}).text.strip()
            credit = {
                'artist': artist,
                'role': role
            }
            credits_list.append(credit)
        return credits_list

    def json(self):
        return self.credits
