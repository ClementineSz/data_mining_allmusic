import re

from scraping.album_credits import AlbumCredits
from scraping.album_details import AlbumDetails
from scraping.config import HtmlTags, HtmlClasses, Patterns

from scraping.utils import protected_from_attribue_error


class Album:
    def __init__(self, soup):
        self.soup = soup
        self.details = AlbumDetails(self)
        self.credits = AlbumCredits(self)

    @property
    @protected_from_attribue_error
    def title(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.TITLE}).text.strip().lower()

    @property
    @protected_from_attribue_error
    def artist(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.ARTIST}).text.strip()

    @property
    @protected_from_attribue_error
    def genre(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.GENRES}).text.strip()

    @property
    @protected_from_attribue_error
    def label(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.LABELS}).text.strip()

    @property
    @protected_from_attribue_error
    def details_url(self):
        return self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.IMAGE}).a['href'].strip()

    @property
    def reference_number(self):
        return re.search(Patterns.REFERENCE_NUMBER, self.details_url).group(1)

    @property
    @protected_from_attribue_error
    def headline_review(self):
        headline_div = self.soup.find(HtmlTags.DIV, {'class': HtmlClasses.HEADLINE_REVIEW})
        return {
            'author': headline_div.find(HtmlTags.DIV, {'class': HtmlClasses.AUTHOR}).text.strip('\n -'),
            'content': headline_div.find(text=True, recursive=False).strip(),
        }

    def json(self):
        return {
            'reference_number': self.reference_number,
            'title': self.title,
            'artist': self.artist,
            'genre': self.genre,
            'label': self.label,
            'details_url': self.details_url,
            'details': self.details.json(),
            'headline_review': self.headline_review,
            'credits': self.credits.json()
        }
