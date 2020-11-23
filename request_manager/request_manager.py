import requests

from request_manager.config import USER_AGENT


def request(url, data=None, post=False, headers=None):
    print(f'Resolving {url} {post}')
    request_headers = {"User-Agent": USER_AGENT}
    if headers is not None:
        request_headers.update(headers)
    if post:
        return requests.post(url, headers=request_headers, data=data)
    return requests.get(url, headers=request_headers, data=data)
