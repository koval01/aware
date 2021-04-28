def link_image(link, video) -> bool:
    """
    Function for image proxy link analyze
    :param link: Analyzing link
    :param video: Video check mode
    :return: Bool result
    """
    if not video:
        s = ['jpg', 'png', 'gif', 'jpeg', 'webp', 'tif', 'tiff']
        l = link.split('.')[-1:]
        return [True for x in s if l[0] == x]
    else:
        return True