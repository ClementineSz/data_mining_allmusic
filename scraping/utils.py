def protected_from_attribue_error(func):
    def wrapper(self):
        try:
            result = func(self)
        except AttributeError:
            return None
        return result

    return wrapper

