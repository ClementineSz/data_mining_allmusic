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
    def get_album_id(album_name):
        access_token = SpotifyApi.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {'q': album_name, 'type': 'album'}
        r = requests.get(SpotifyEndpoints.ALBUM_SEARCH, params=params, headers=headers)
        return r.json()

    @staticmethod
    def get_access_token():
        logger.info("Getting access token")

        base64_bytes = get_encoded_client_data()

        headers = {'Authorization': f"Basic {base64_bytes.decode('ascii')}"}
        data = {'grant_type': 'client_credentials'}

        result = requests.post(SpotifyEndpoints.API_TOKEN, data=data, headers=headers)
        access_token = result.json().get('access_token')
        return access_token
