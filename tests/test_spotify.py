import os

from spotify_api.request_data_api import SpotifyApi


def test_get_client_id():
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    print(client_id)
    assert client_id is not None


def test_get_client_secret():
    client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    print(client_secret)
    assert client_secret is not None


def test_get_access_token():
   api = SpotifyApi()
   api.get_authorization()


#def test_get_album_popularity(spotify_album_id):