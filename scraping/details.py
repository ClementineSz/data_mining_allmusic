from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from request_manager import request_manager
from request_manager.request_manager import fetch
from scraping.reviews import Reviews
from scraping.config import Endpoints, HtmlTags, HtmlClasses
from scraping.track import Track
from scraping.utils import protected_from_attribute_error, to_title, strip


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
    @protected_from_attribute_error
    def duration(self):
        """
        Extracts duration from the html
        @return:
        """
        string = self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.DURATION}).span.text.strip()
        try:
            time = datetime.strptime(string, '%M:%S')
        except ValueError:
            time = datetime.strptime(string, '%H:%M:%S')

        seconds = timedelta(seconds=time.second, minutes=time.minute).seconds
        return seconds

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def genre(self):
        """
        Extracts genre from the html
        @return:
        """
        return self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.GENRE}).a.text.strip()

    @property
    def review_url(self):
        return request_manager.create_url(Endpoints.ALBUM, Endpoints.FETCH_REVIEW_VIEW, self.album.reference_number)

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def styles(self):
        """ Extracts styles from the html
        @return:
        """
        styles_div = self.soup.find(HtmlTags.DIV, {"class": HtmlClasses.STYLES})
        styles_a = styles_div.find_all(HtmlTags.A)
        return [style.text.strip() for style in styles_a]

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def moods(self):
        """ Extracts moods from the html
        @return:
        """
        moods_div = self.soup.find(HtmlTags.SECTION, {"class": HtmlClasses.MOODS})
        mood_spans = moods_div.find_all(HtmlTags.SPAN, {"class": HtmlClasses.MOOD})
        return [mood.text.lower().strip() for mood in mood_spans]

    @property
    @protected_from_attribute_error
    @to_title
    @strip
    def themes(self):
        """ Extracts themes from the html
        @return:
        """
        themes_div = self.soup.find(HtmlTags.SECTION, {"class": HtmlClasses.THEMES})
        theme_spans = themes_div.find_all(HtmlTags.SPAN, {"class": HtmlClasses.THEME})
        return [theme.text.lower().strip() for theme in theme_spans]

    @property
    @protected_from_attribute_error
    def review_body(self):
        """ Extracts review_body from the html
        @return:
        """
        return self.soup.find(HtmlTags.DIV, {'itemprop': HtmlClasses.REVIEW_BODY}).text.strip()

    @property
    @protected_from_attribute_error
    def tracks(self):
        """ Extracts tracks from the html
        @return:
        """
        track_listing_divs = self.soup.find_all(HtmlTags.TR, {"class": HtmlClasses.TRACK})
        tracks = [Track(track_div) for track_div in track_listing_divs]
        return tracks

    @property
    @protected_from_attribute_error
    def user_ratings(self):
        """ Extracts user_ratings from the html
        @return:
        """
        user_ratings_div = self.soup.find(HtmlTags.UL, {"class": HtmlClasses.RATINGS})
        classes = self.soup.find(HtmlTags.UL, {"class": HtmlClasses.RATINGS}).find(HtmlTags.DIV, {
            "class": HtmlClasses.AVERAGE_USER_RATING})['class']
        # rating_class = classes[-1]
        return {
            'number': user_ratings_div.find('span', {"class": HtmlClasses.USER_RATING_COUNT}).contents[0],
            # 'ratings' : re.search('([0-9])', rating_class).group(1)
        }
