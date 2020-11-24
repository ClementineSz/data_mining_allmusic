from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from request_manager import request_manager
from request_manager.request_manager import fetch
from scraping.reviews import Reviews
from scraping.config import Endpoints, HtmlTags, HtmlClasses
from scraping.utils import protected_from_attribue_error


class Details:
    def __init__(self, album):
        self.album = album
        self.reviews = Reviews(self)
        self.soup = self.load_soup()

    def load_soup(self):
        url = Endpoints.BASE + self.album.details_url
        response = fetch(url)
        return BeautifulSoup(response.text, 'html.parser')

    @property
    @protected_from_attribue_error
    def duration(self):
        string = self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.DURATION}).span.text.strip()
        try:
            time = datetime.strptime(string, '%M:%S')
        except ValueError:
            time = datetime.strptime(string, '%H:%M:%S')

        seconds = timedelta(seconds=time.second, minutes=time.minute).seconds
        return seconds

    @property
    @protected_from_attribue_error
    def genre(self):
        return self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.GENRE}).a.text.strip()

    @property
    def review_url(self):
        return request_manager.create_url(Endpoints.ALBUM, Endpoints.FETCH_REVIEW_VIEW, self.album.reference_number)

    @property
    @protected_from_attribue_error
    def styles(self):
        styles_div = self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.STYLES})
        styles_a = styles_div.find_all(HtmlTags.A)
        return [style.text.strip() for style in styles_a]

    @property
    @protected_from_attribue_error
    def moods(self):
        moods_div = self.soup.find(HtmlTags.SECTION, {"class": HtmlClasses.MOODS})
        mood_spans = moods_div.find_all(HtmlTags.SPAN, {"class": HtmlClasses.MOOD})
        return [mood.text.lower().strip() for mood in mood_spans]

    @property
    @protected_from_attribue_error
    def themes(self):
        themes_div = self.soup.find(HtmlTags.SECTION, {"class": HtmlClasses.THEMES})
        theme_spans = themes_div.find_all(HtmlTags.SPAN, {"class": HtmlClasses.THEME})
        return [theme.text.lower().strip() for theme in theme_spans]

    @property
    @protected_from_attribue_error
    def review_body(self):
        return self.soup.find(HtmlTags.DIV, {'itemprop': HtmlClasses.REVIEW_BODY}).text.strip()

    @property
    @protected_from_attribue_error
    def track_listing(self):
        track_listing_divs = self.soup.find_all(HtmlTags.TR, {"class": HtmlClasses.TRACK})
        tracks = []
        for track_listing_div in track_listing_divs:
            tracknum = track_listing_div.find(HtmlTags.TD, {'class': HtmlClasses.TRACKNUM}).text.strip()
            title = track_listing_div.find(HtmlTags.DIV, {'class': HtmlClasses.TITLE}).text.strip()
            composer = track_listing_div.find(HtmlTags.DIV, {'class': HtmlClasses.COMPOSER}).text.strip()
            performer = track_listing_div.find(HtmlTags.TD, {'class': HtmlClasses.PERFORMER}).text.strip()
            try:
                time_string = track_listing_div.find(HtmlTags.TD, {'class': HtmlClasses.TIME}).text.strip()
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
    @protected_from_attribue_error
    def user_ratings(self):
        user_ratings_div = self.soup.find(HtmlTags.UL, {"class": HtmlClasses.RATINGS})
        classes = self.soup.find(HtmlTags.UL, {"class": HtmlClasses.RATINGS}).find(HtmlTags.DIV, {
            "class": HtmlClasses.AVERAGE_USER_RATING})['class']
        # rating_class = classes[-1]
        return {
            'number': user_ratings_div.find('span', {"class": HtmlClasses.USER_RATING_COUNT}).contents[0],
            # 'ratings' : re.search('([0-9])', rating_class).group(1)
        }
