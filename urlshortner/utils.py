import random


def get_shorturl(thing_object, url_length, filter_kwargs=None, check_for_existing_var=None):
    # generates unique (or not, if check_for_existing == False) character-set of length [url_length] with
    # alphabet [alphabet]. Checks if unique or not in thing_object.objects class

    if filter_kwargs is None:
        filter_kwargs = {}
    alphabet = 'abcdefghjklmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789-'

    unique = False
    short_code = ''
    max_tries = 2  # How much requests to database, till we will give up on url_length and add 1 symbol to it
    tries = 0
    while not unique:
        tries += 1
        short_code = ''.join([random.choice(alphabet) for i in range(url_length)])
        if check_for_existing_var:
            filter_kwargs.update({check_for_existing_var: short_code})
        if not thing_object.objects.filter(**filter_kwargs).exists():
            unique = True
        if tries > max_tries:
            url_length += 1
            tries = 0

    return short_code


