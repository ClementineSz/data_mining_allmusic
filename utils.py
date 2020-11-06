import requests

from models.constants import USER_AGENT


def make_request(url, post=False, data=None):
    print(f'Resolving {url} {post}')
    headers = {"User-Agent": USER_AGENT}

    if post:
        return requests.post(url, headers=headers, data=data)
    return requests.get(url, headers=headers, data=data)