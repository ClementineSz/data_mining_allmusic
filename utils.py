import requests

from models.constants import USER_AGENT


def make_request(url, post=False):
    print(f'Resolving {url} {post}')
    headers = {"User-Agent": USER_AGENT}

    if post:
        return requests.post(url, headers=headers)
    return requests.get(url, headers=headers)