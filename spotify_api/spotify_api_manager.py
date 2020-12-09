import json
import logging
import os
import sys


import requests
from spotify_api.config import SpotifyEndpoints, SpotifyConstants

logger = logging.getLogger('spotify_api')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


class SpotifyApi:

    @property
    def access_token(self):
        logger.info("Getting access token")
        data = dict()
        data['grant_type'] = 'client_credentials'
        headers = dict()
        import base64

        authorization = f"{os.environ['SPOTIFY_CLIENT_ID']}:{os.environ['SPOTIFY_CLIENT_SECRET']}"
        message_bytes = authorization.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)

        headers['Authorization'] = f"Basic {base64_bytes.decode('ascii')}"

        result = requests.post(SpotifyEndpoints.API_TOKEN, data=data, headers=headers)
        access_token = result.json().get('access_token')
        return access_token
