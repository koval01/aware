from PIL import Image
from requests import get
from django.conf import settings
import logging, os

logger = logging.getLogger(__name__)
base_dir = settings.BASE_DIR
font_root = os.path.join(base_dir, 'my_web/fonts_for_Pillow/Roboto-Light.ttf')


def get_image() -> dict:
    """
    Get image from Unsplash source
    :return: raw image template
    """
    url = 'https://source.unsplash.com/random/1600x900'
    try:
        img = get(url, stream=True)
        return dict(
            img=img.raw,
            status_code=img.status_code,
            reason=img.reason,
            headers=img.headers.get('content-type'),
        )
    except Exception as e:
        logger.error(e)


def image_edit(image_raw, text) -> str:
    """
    Prepare an image using Pillow library
    :param image_raw: raw image to edit
    :param text: The text you want to overlay on the image
    :return: the finished image, which is also translated into raw
    """
    try:
        img = Image.open(image_raw)
    except Exception as e:
        logger.error(e)
        logger.error('error pillow')


def get_result(text) -> dict:
    """
    Request image processing
    :param text: The text you want to overlay on the image
    :return: The finished image in raw
    """
    img = get_image()
    result = image_edit(img['img'], text)
    return dict(
        img=result,
        status_code=img['status_code'],
        reason=img['reason'],
        headers=img['headers'],
    )