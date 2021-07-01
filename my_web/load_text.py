from random import choice


def get_text() -> str:
    """
    Random text load button
    :return: text
    """
    list_text = [
        'Loading',
        'Updating',
        'Preparing',
    ]
    return choice(list_text)+'...'