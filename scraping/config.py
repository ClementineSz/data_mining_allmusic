class Endpoints:
    BASE = 'https://www.allmusic.com'
    NEW_RELEASES = 'newreleases'
    ALBUM = 'album'
    FETCH_REVIEW_VIEW = 'fetch_review_view'
    USER_REVIEWS = 'user-reviews'
    CREDITS = 'credits'


class HtmlClasses:
    NEW_RELEASE = 'new-release'
    CREDIT = 'credit'
    AVERAGE_USER_RATING = "average-user-rating"
    USER_REVIEW = "user_review"
    GENRE = 'genre'
    DURATION = 'duration'
    MIDDLE = 'middle'
    DATA = "data"
    PROFILE_USER_RATING = "profile-user-rating"
    USER_RATING_COUNT = "average-user-rating-count"
    RATINGS = "ratings"
    CREDITS = "credits"
    AUTHOR = "author"
    HEADLINE_REVIEW = "headline-review"
    IMAGE = "image-container"
    LABELS = "labels"
    GENRES = "genres"
    ARTIST = "artist"
    TITLE = "title"
    TIME = 'time'
    PERFORMER = 'performer'
    COMPOSER = 'composer'
    TRACKNUM = 'tracknum'
    TRACK = "track"
    REVIEW_BODY = 'reviewBody'
    THEME = "theme"
    THEMES = "themes"
    MOOD = "mood"
    MOODS = "moods"
    STYLES = "styles"


class HtmlTags:
    P = 'p'
    UL = 'ul'
    SPAN = 'span'
    A = 'a'
    SECTION = 'section'
    DIV = 'div'
    TD = 'td'
    TR = 'tr'


class Patterns:
    REFERENCE_NUMBER = '.*-(.*)'
    REVIEW_RATING = '([0-9])'
