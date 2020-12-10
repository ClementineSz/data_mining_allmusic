import json
import logging
import os
import sys
import base64
import requests
from spotify_api.config import SpotifyEndpoints, SpotifyConstants

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger('main.spotify_api')


def get_encoded_client_data():
    authorization = f"{os.environ['SPOTIFY_CLIENT_ID']}:{os.environ['SPOTIFY_CLIENT_SECRET']}"
    message_bytes = authorization.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    return base64_bytes


class SpotifyArtistNotFoundError(Exception):
    pass


class SpotifyAlbumNotFoundError(Exception):
    pass


class SpotifyApi:
    access_token = None

    @staticmethod
    def get_access_token():
        """ Get the access token for the api

        @return: access token
        """

        if SpotifyApi.access_token is not None:
            return SpotifyApi.access_token
        logger.info("Getting access token")
        base64_bytes = get_encoded_client_data()

        headers = {'Authorization': f"Basic {base64_bytes.decode('ascii')}"}
        data = {'grant_type': 'client_credentials'}

        result = requests.post(SpotifyEndpoints.API_TOKEN, data=data, headers=headers)
        access_token = result.json().get('access_token')
        SpotifyApi.access_token = access_token
        return SpotifyApi.access_token

    @staticmethod
    def get_album_id(album_name, artist_name):
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        query = f"{album_name} artist:{artist_name}"
        params = {'q': query, 'type': 'album', 'limit': 1}
        r = requests.get(SpotifyEndpoints.SEARCH, params=params, headers=headers)
        parsed = r.json()
        albums = parsed.get('albums').get('items')
        try:
            first_result = albums[0]
        except IndexError:
            logger.error(f'No information on Spotify for {album_name}')
            raise SpotifyAlbumNotFoundError()
        album_id = first_result.get('id')

        return album_id

    @staticmethod
    def get_album_info(album_title, album_artist_name):
        """

        @param album_title:
        @param album_artist_name:
        """
        logger.info(f'Fetching album {album_title}')

        album_id = SpotifyApi.get_album_id(album_title, album_artist_name)

        full_album = SpotifyApi.get_full_album_info(album_id)

        popularity = full_album.get('popularity')

        return {
            'popularity': popularity,
        }

    @staticmethod
    def get_artist_id(artist_name):
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        query = f"{artist_name}"
        params = {'q': query, 'type': 'artist', 'limit': 1}
        r = requests.get(SpotifyEndpoints.SEARCH, params=params, headers=headers)
        artists = r.json().get('artists').get('items')
        try:
            artist = artists[0]
        except IndexError:
            logger.error(f'No information on Spotify for {artist_name}')
            raise SpotifyArtistNotFoundError()
        return artist.get('id')

    @staticmethod
    def get_artist_info(artist_name):
        logger.info(f'Fetching artist {artist_name}')
        artist_id = SpotifyApi.get_artist_id(artist_name)
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        url = SpotifyEndpoints.ARTIST + artist_id
        r = requests.get(url, headers=headers)
        parsed = r.json()

        popularity = parsed.get('popularity')
        name = parsed.get('name')
        followers = parsed.get('followers').get('total')

        return {'name': name, 'popularity': popularity, 'followers': followers}

    @staticmethod
    def get_full_album_info(album_id):

        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        url = SpotifyEndpoints.ALBUM + album_id
        r = requests.get(url, headers=headers)
        return r.json()
