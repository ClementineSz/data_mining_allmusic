import base64
import logging
import os
import time

import requests
from dotenv import load_dotenv

from spotify_api.config import SpotifyEndpoints

load_dotenv()
logger = logging.getLogger('main')


def get_encoded_client_data():
    """ Encode the authorization url to send to the api

    @return: encode authorization
    """
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

        logger.info("Getting access token")
        base64_bytes = get_encoded_client_data()

        headers = {'Authorization': f"Basic {base64_bytes.decode('ascii')}"}
        data = {'grant_type': 'client_credentials'}

        result = requests.post(SpotifyEndpoints.API_TOKEN, data=data, headers=headers)
        access_token = result.json().get('access_token')
        SpotifyApi.access_token = access_token

    @staticmethod
    def get_album_id(album_name, artist_name):
        """ Get the album id from the search request which take as parameter the album name from allmusing

        @param album_name:
        @param artist_name:
        @return: album id from spotify
        """
        SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {SpotifyApi.access_token}"}
        query = f"{album_name} artist:{artist_name}"
        params = {'q': query, 'type': 'album', 'limit': 1}

        url = SpotifyEndpoints.SEARCH
        response = SpotifyApi.fetch(url, params=params, headers=headers)
        albums = response.get('albums').get('items')
        try:
            first_result = albums[0]
        except IndexError:
            logger.warning(f'No information on Spotify for {album_name}')
            raise SpotifyAlbumNotFoundError()
        album_id = first_result.get('id')

        return album_id

    @staticmethod
    def get_album_info(album_title, album_artist_name):
        """ Get the popularity of the album in spotify

        @param album_title:
        @param album_artist_name:
        """
        logger.debug(f'Fetching album {album_title}')

        album_id = SpotifyApi.get_album_id(album_title, album_artist_name)

        full_album = SpotifyApi.get_full_album_info(album_id)

        popularity = full_album.get('popularity')

        return {
            'popularity': popularity,
        }

    @staticmethod
    def get_artist_id(artist_name):
        """ Get the artist id from spotify from search request

        @param artist_name:
        @return:
        """
        SpotifyApi.get_access_token()

        headers = {"Authorization": f"Bearer {SpotifyApi.access_token}"}
        query = f"{artist_name}"
        params = {'q': query, 'type': 'artist', 'limit': 1}
        url = SpotifyEndpoints.SEARCH
        response = SpotifyApi.fetch(url, params=params, headers=headers)

        artists = response.get('artists').get('items')
        try:
            artist = artists[0]
        except IndexError:
            logger.warning(f'No information on Spotify for {artist_name}')
            raise SpotifyArtistNotFoundError()
        return artist.get('id')

    @staticmethod
    def get_artist_info(artist_name):
        """ Get popularity, followers from artist

        @param artist_name:
        @return: popularity and followers in spotify
        """
        logger.debug(f'Fetching artist {artist_name}')
        artist_id = SpotifyApi.get_artist_id(artist_name)
        SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {SpotifyApi.access_token}"}
        url = SpotifyEndpoints.ARTIST + artist_id

        parsed = SpotifyApi.fetch(url, headers)

        popularity = parsed.get('popularity')
        name = parsed.get('name')
        followers = parsed.get('followers').get('total')

        return {'name': name, 'popularity': popularity, 'followers': followers}

    @staticmethod
    def fetch(url, params=None, headers=None):
        retries = 3
        while True:
            if retries == 0:
                logger.error("Can't access Spotify API")
                raise RuntimeError
            r = requests.get(url, params=params, headers=headers)
            logger.info(r.status_code)
            if r.status_code != 200:
                duration = 1
                if r.status_code == 429:
                    duration = int(r.headers.get('Retry-After'))
                    logger.warning(f"Rate limit reached, sleeping for {duration}")
                    time.sleep(duration)
                retries -= 1
                SpotifyApi.get_access_token()
                time.sleep(duration)
                continue

            return r.json()

    @staticmethod
    def get_full_album_info(album_id):
        """ Get the json from the spotify api with all information of an album

        @param album_id:
        @return: json with information of an album
        """
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        url = SpotifyEndpoints.ALBUM + album_id

        response = SpotifyApi.fetch(url, headers=headers)

        return response
