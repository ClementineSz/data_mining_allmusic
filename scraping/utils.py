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
