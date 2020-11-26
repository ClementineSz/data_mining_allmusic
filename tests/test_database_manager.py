from database.database_manager import sql_session, create_tables, drop_tables, get_or_create
from models.album import Album as ModelAlbum, Artist, Label, Mood, Theme, Style, Track, ReviewBody, Genre, Review, \
    Credit, Role
from scraping.album import Album as ScrapingAlbum
from scraping.allmusic_scraper import get_albums_html


def test_album_model():
    session = sql_session()

    albums_html = get_albums_html()

    album = ScrapingAlbum(albums_html.pop(0))

    artist = get_or_create(session, Artist, name=album.artist_name)
    label = get_or_create(session, Label, name=album.label)
    styles = [get_or_create(session, Style, description=style) for style in album.details.styles]
    moods = [get_or_create(session, Mood, description=mood) for mood in album.details.moods]
    themes = [get_or_create(session, Theme, description=theme) for theme in album.details.themes]
    genre = get_or_create(session, Genre, description=album.details.genre)

    tracks = []
    for track in album.details.tracks:
        track_model = get_or_create(session, Track, title=track.title)
        composer = get_or_create(session, Artist, name=track.composer)
        track_model.duration = track.duration
        track_model.composer = composer
        tracks.append(track_model)

    reviews = [get_or_create(session, Review, content=review.content, author=review.author, date=review.date) for review
               in
               album.details.reviews]

    credits = []
    for credit in album.credits:
        for role in credit.roles:
            credits.append(
                get_or_create(session, Credit, artist=get_or_create(session, Artist, name=credit.artist_name),
                              role=get_or_create(session, Role, name=role)))

    review_body = get_or_create(session, ReviewBody, content=album.details.review_body)
    model_album = get_or_create(session, ModelAlbum, reference_number=album.reference_number)

    model_album.review_body = review_body
    model_album.title = album.title
    model_album.artist = artist
    model_album.label = label
    model_album.headline_review_author = album.headline_review.author
    model_album.headline_review_content = album.headline_review.content
    model_album.moods = moods
    model_album.styles = styles
    model_album.themes = themes
    model_album.genre = genre
    model_album.reviews = reviews
    model_album.tracks = tracks
    model_album.credits = credits

    session.add(model_album)
    session.commit()


def test_create_table():
    create_tables()


def test_drop_table():
    drop_tables()


def test_refresh_tables():
    create_tables()
    drop_tables()


def test_refresh_and_insert():
    drop_tables()
    create_tables()
    test_album_model()
