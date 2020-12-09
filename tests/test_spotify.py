import os

from spotify_api.spotify_api_manager import SpotifyApi


def test_get_client_id():
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    print(client_id)
    assert client_id is not None


def test_get_client_secret():
    client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    print(client_secret)
    assert client_secret is not None


def test_get_access_token():
    album_id = SpotifyApi.get_album_id('Moment', 'Dark Tranquillity')
    print(album_id)


def test_get_artist_info():
    info = SpotifyApi.get_album_info('Moment', 'Dark Tranquillity')