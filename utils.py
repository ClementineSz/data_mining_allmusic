import pprint

import requests

from models.constants import USER_AGENT


def soup_extractor(func):
    def wrapper(self):
        print("Something is happening before the function is called.")
        result = func(self)
        print("Something is happening after the function is called.")
        return result
    try:
        return wrapper
    except AttributeError:
        return None


def make_request(url, data=None, post=False, headers=None):
    print(f'Resolving {url} {post}')
    request_headers = {"User-Agent": USER_AGENT}
    if headers is not None:
        request_headers.update(headers)
    if post:
        return requests.post(url, headers=request_headers, data=data)
    return requests.get(url, headers=request_headers, data=data)


def pretty_print(string):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(string)
