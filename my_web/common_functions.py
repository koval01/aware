def get_random_string(length=16) -> str:
    """
    Random string generator function
    :param length: length string
    :return: generated string
    """
    letters = string.ascii_letters + string.digits + '_-'
    return ''.join(choice(letters) for i in range(length))