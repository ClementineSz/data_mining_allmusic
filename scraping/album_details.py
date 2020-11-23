from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import re
from scraping.album_reviews import AlbumReviews
from scraping.config import BASE_URL, NEW_RELEASES_ENDPOINT, ALBUM_ENDPOINT, FETCH_REVIEW_ENDPOINT
from utils import request, soup_extractor


class AlbumDetails:
    def __init__(self, album):
        self.album = album
        self.reviews = AlbumReviews(self)
        self.soup = self.load_soup()

    def load_soup(self):
        url = BASE_URL + self.album.details_url
        response = request(url)
        return BeautifulSoup(response.text, 'html.parser')

    @property
    @soup_extractor
    def duration(self):
        string = self.soup.find('div', {"class": "duration"}).span.text.strip()
        try:
            time = datetime.strptime(string, '%M:%S')
        except ValueError:
            time = datetime.strptime(string, '%H:%M:%S')

        seconds = timedelta(seconds=time.second, minutes=time.minute).seconds
        return seconds

    @property
    @soup_extractor
    def genre(self):
        return self.soup.find('div', {"class": "genre"}).a.text.strip()

    @property
    def review_url(self):
        return ALBUM_ENDPOINT + FETCH_REVIEW_ENDPOINT + self.album.id

    @property
    @soup_extractor
    def styles(self):
        styles_div = self.soup.find('div', {"class": "styles"})
        styles_a = styles_div.find_all('a')
        return [style.text.strip() for style in styles_a]

    @property
    @soup_extractor
    def moods(self):
        moods_div = self.soup.find('section', {"class": "moods"})
        mood_spans = moods_div.find_all('span', {"class": "mood"})
        return [mood.text.lower().strip() for mood in mood_spans]

    @property
    @soup_extractor
    def themes(self):
        themes_div = self.soup.find('section', {"class": "themes"})
        theme_spans = themes_div.find_all('span', {"class": "theme"})
        return [theme.text.lower().strip() for theme in theme_spans]

    @property
    @soup_extractor
    def review_body(self):
        return self.soup.find('div', {'itemprop': 'reviewBody'}).text.strip()

    @property
    @soup_extractor
    def track_listing(self):
        track_listing_divs = self.soup.find_all('tr', {"class": "track"})
        tracks = []
        for track_listing_div in track_listing_divs:
            tracknum = track_listing_div.find('td', {'class': 'tracknum'}).text.strip()
            title = track_listing_div.find('div', {'class': 'title'}).text.strip()
            composer = track_listing_div.find('div', {'class': 'composer'}).text.strip()
            performer = track_listing_div.find('td', {'class': 'performer'}).text.strip()
            try:
                time_string = track_listing_div.find('td', {'class': 'time'}).text.strip()
                time = datetime.strptime(time_string, '%M:%S')
                seconds = timedelta(seconds=time.second, minutes=time.minute).seconds

            except ValueError:
                seconds = None
            track = {
                'tracknum': tracknum,
                'title': title,
                'composer': composer,
                'performer': performer,
                'duration': seconds,
            }
            tracks.append(track)
        return tracks

    @property
    @soup_extractor
    def user_ratings(self):
        user_ratings_div = self.soup.find('ul', {"class": RATINGS})
        classes = self.soup.find('ul', {"class": "ratings"}).find('div', {"class": "average-user-rating"})['class']
        # rating_class = classes[-1]
        return {
            'number': user_ratings_div.find('span', {"class": USER_RATING_COUNT}).contents[0],
            # 'ratings' : re.search('([0-9])', rating_class).group(1)
        }

    def json(self):
        return {
            'track_listing': self.track_listing,
            'review_body': self.review_body,
            'themes': self.themes,
            'moods': self.moods,
            'styles': self.styles,
            'duration': self.duration,
            'genre': self.genre,
            'review_url': self.review_url,
            'reviews': self.reviews.json(),
            'user_ratings': self.user_ratings
        }