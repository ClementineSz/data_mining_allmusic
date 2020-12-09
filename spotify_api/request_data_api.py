import logging
import os

import requests
from spotify_api.config import SpotifyEndpoints, SpotifyConstants

logger = logging.getLogger('spotify_api')

class SpotifyApi:

    def get_authorization(self):
        params = dict()
        params['response_type'] = 'code'
        params['client_id'] = os.environ['SPOTIFY_CLIENT_ID']
        params['client_secret'] = os.environ['SPOTIFY_CLIENT_SECRET']
        params['redirect_uri'] = SpotifyConstants.REDIRECT_URI
        result = requests.get(SpotifyEndpoints.AUTHORIZE, params=params)
        return result



