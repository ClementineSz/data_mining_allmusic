from bs4 import BeautifulSoup

from models.constants import BASE_URL, ALBUM, CREDITS
from utils import make_request

CREDITS_ = "credits"


class AlbumCredits:
    def __init__(self, album):
        self.album = album
        self.soup = self.load_soup()

    def load_soup(self):
        url = BASE_URL + self.album.details_url + CREDITS
        print(url)
        response = make_request(url)
        return BeautifulSoup(response.text, 'html.parser')

    @property
    def credits(self):
        section_credits = self.soup.find('section', {"class": CREDITS_})
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
