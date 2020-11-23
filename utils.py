import pprint

import requests

from scraping.config import USER_AGENT


def soup_extractor(func):
    def wrapper(self):
        try:
            result = func(self)
        except AttributeError:
            return None
        return result
    return wrapper




def pretty_print(string):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(string)
