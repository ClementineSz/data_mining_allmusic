from scraping.artist import Artist


def test_scraping_artist():
    artist = Artist('test')
    artist.popularity = 100
    print(artist.popularity)
    assert artist.popularity == 100
