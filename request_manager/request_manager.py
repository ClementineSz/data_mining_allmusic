import requests

from request_manager.config import USER_AGENT


def fetch(url, data=None, post=False, headers=None):
    print(f'{"POST" if post else "GET"} - \"{url}\"')
    request_headers = {"User-Agent": USER_AGENT}
    if headers is not None:
        request_headers.update(headers)
    if post:
        return requests.post(url, headers=request_headers, data=data)
    return requests.get(url, headers=request_headers, data=data)


def create_url(*args):
    return '/'.join(args)