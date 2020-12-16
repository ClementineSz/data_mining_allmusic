import logging

import requests

from scraping.config import Endpoints

logger = logging.getLogger('main')

def protected_from_attribute_error(func):
    """  Decorator which catch Attributeerror and return None instead

    @param func:
    @return:
    """

    def wrapper(self):
        try:
            result = func(self)
        except AttributeError:
            return None
        return result

    return wrapper


def to_title(func):
    def wrapper(self):
        result = func(self)
        if type(result) is list:
            return [element.title() for element in result]
        return result.title()

    return wrapper


def strip(func):
    def wrapper(self):
        result = func(self)
        if type(result) is list:
            return [element.strip() for element in result]
        return result.strip()

    return wrapper

def fetch(url, data=None, post=False, headers=None):
    """ Send a post or get request with headers

    @param url:
    @param data:
    @param post:
    @param headers:
    @return:
    """
    logger.debug(f'{"POST" if post else "GET"} - \"{url}\"')
    request_headers = {"User-Agent": Endpoints.USER_AGENT}
    if headers is not None:
        request_headers.update(headers)
    if post:
        return requests.post(url, headers=request_headers, data=data)
    return requests.get(url, headers=request_headers, data=data)


def create_url(*args):
    return '/'.join(args)
