def link_image(link) -> bool:
    """
    Function for image proxy link analyze
    :param link: Analyzing link
    :return: Bool result
    """
    s = ['jpg', 'png', 'gif', 'jpeg', 'webp', 'tif', 'tiff']
    l = link.split('.')[-1:]
    return [True for x in s if l[0] == x]