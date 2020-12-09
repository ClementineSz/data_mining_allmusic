import json
import logging
import os
import sys
import base64
import requests
from spotify_api.config import SpotifyEndpoints, SpotifyConstants

logger = logging.getLogger('spotify_api')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def get_encoded_client_data():
    authorization = f"{os.environ['SPOTIFY_CLIENT_ID']}:{os.environ['SPOTIFY_CLIENT_SECRET']}"
    message_bytes = authorization.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes


class SpotifyApi:

    @staticmethod
    def get_access_token():
        """ Get the access token for the api

        @return: access token
        """
        logger.info("Getting access token")

        base64_bytes = get_encoded_client_data()

        headers = {'Authorization': f"Basic {base64_bytes.decode('ascii')}"}
        data = {'grant_type': 'client_credentials'}

        result = requests.post(SpotifyEndpoints.API_TOKEN, data=data, headers=headers)
        access_token = result.json().get('access_token')
        return access_token

    @staticmethod
    def get_album_id(album_name, artist_name):
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        query = f"{album_name} artist:{artist_name}"
        params = {'q': query, 'type': 'album', 'limit': 1}
        r = requests.get(SpotifyEndpoints.ALBUM_SEARCH, params=params, headers=headers)
        parsed = r.json()
        albums = parsed.get('albums').get('items')
        first_result = albums[0]
        album_id = first_result.get('id')

        logger.info(f'Got album id for {album_name} by {artist_name}')
        return album_id

    @staticmethod
    def get_artist_id(album_title, album_artist):
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        spotify_id = SpotifyApi.get_album_id(album_title, album_artist)
        url = SpotifyEndpoints.ALBUM + spotify_id
        r = requests.get(url, headers=headers)
        parsed = r.json()
        artists = parsed.get('artists')
        artist_id = artists[0].get('id')
        logger.info(f'Got artist id for {album_title} by {album_artist}')
        return artist_id

    @staticmethod
    def get_album_popularity(album_title, album_artist):
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        spotify_id = SpotifyApi.get_album_id(album_title, album_artist)
        url = SpotifyEndpoints.ALBUM + spotify_id
        r = requests.get(url, headers=headers)
        parsed = r.json()
        popularity = parsed.get('popularity')
        logger.info(f'Got popularity for {album_title} by {album_artist}')
        return popularity

    @staticmethod
    def get_artist_popularity(album_title, album_artist):
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        spotify_artist_id = SpotifyApi.get_artist_id(album_title, album_artist)
        url = SpotifyEndpoints.ARTIST + spotify_artist_id
        r = requests.get(url, headers=headers)
        parsed = r.json()
        artist_popularity = parsed.get('popularity')
        logger.info(f'Got popularity for {album_artist}')
        return artist_popularity

    @staticmethod
    def get_artist_followers(album_title, album_artist):
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        spotify_artist_id = SpotifyApi.get_artist_id(album_title, album_artist)
        url = SpotifyEndpoints.ARTIST + spotify_artist_id
        r = requests.get(url, headers=headers)
        parsed = r.json()
        artist_followers = parsed.get('followers')
        logger.info(f'Got followers for {album_artist}')
        return artist_followers

    @staticmethod
    def get_album_info(self, album_title, album_artist_name):
        """

        @param album_title:
        @param album_artist_name:
        """

        album_spotify_info = dict()
        album_spotify_info['popularity'] = SpotifyApi.get_album_popularity(album_title, album_artist_name)
        # for
        #
        #
        #     'popularity': 45,
        #     'artists': {'Rihanna': {'popularity': 90, 'followers': 140},
        #                 'EMINEM': {'popularity': 90, 'followers': 140}}
        # }
