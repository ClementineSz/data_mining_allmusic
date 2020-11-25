from database.database_manager import sql_session, create_tables, drop_tables
from models.album import Album as ModelAlbum, Artist, Label, Mood, Theme, Style, Track, ReviewBody, Genre, Review, \
    Credit
from scraping.album import Album as ScrapingAlbum
from scraping.allmusic_scraper import get_albums_html


def test_album_model():
    albums_html = get_albums_html()

    album = ScrapingAlbum(albums_html.pop(0))

    artist = Artist(name=album.artist)
    label = Label(name=album.label)
    styles = [Style(description=style) for style in album.details.styles]
    moods = [Mood(description=mood) for mood in album.details.moods]
    themes = [Theme(description=theme) for theme in album.details.themes]
    genre = Genre(description=album.details.genre)
    tracks = [Track(title=track.title, duration=track.duration) for track in
              album.details.tracks]

    reviews = [Review(content=review.content, author=review.author, date=review.date) for review in
               album.details.reviews]

    credits = [Credit(artist=credit.artist, role=credit.role) for credit in album.credits]
    review_body = ReviewBody(content=album.details.review_body)
    model_album = ModelAlbum(reference_number=album.reference_number,
                             review_body=review_body,
                             title=album.title,
                             artist=artist,
                             label=label,
                             headline_review_author=album.headline_review.author,
                             moods=moods,
                             styles=styles,
                             themes=themes,
                             genre=genre)
    model_album.reviews = reviews
    model_album.tracks = tracks
    model_album.credits = credits
    session = sql_session()
    session.add(model_album)
    session.commit()


def test_create_table():
    create_tables()


def test_drop_table():
    drop_tables()
