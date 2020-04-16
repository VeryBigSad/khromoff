class NameExistsError(Exception):
    # Alias already exists
    def __init__(self, msg=None):
        if msg is None:
            msg = 'This alias you are trying to use already exists. Try another!'


class InvalidAliasError(Exception):
    # You can't use such alias
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Alias you are trying to use can\'t be used. Try another.'


class InvalidUrlError(Exception):
    # Long url passed in is invalid
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Long URL you passed in is invalid, maybe a typo?'

