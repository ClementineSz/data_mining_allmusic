import pprint


def pretty_print(string):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(string)
