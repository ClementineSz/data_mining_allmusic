import requests

from models.constants import USER_AGENT


def get_request(url):
    print(f'Resolving {url}')

    headers = {"User-Agent": USER_AGENT}
    return requests.get(url, headers=headers)