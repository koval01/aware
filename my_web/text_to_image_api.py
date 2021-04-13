from PIL import Image, ImageFilter, ImageDraw, ImageFont
from io import BytesIO
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
    url = 'https://source.unsplash.com/collection/4900654/1600x900'
    try:
        img = get(url, stream=True)
        return dict(
            img=img.content,
            status_code=img.status_code,
            reason=img.reason,
            headers=img.headers.get('content-type'),
        )
    except Exception as e:
        logger.error(e)


def image_edit(image, text) -> bytes:
    """
    Prepare an image using Pillow library
    :param image: image to edit
    :param text: The text you want to overlay on the image
    :return: the finished image, which is also translated into raw
    """
    img = Image.open(BytesIO(image))

    blured_image = img.filter(ImageFilter.GaussianBlur(15))
    text_config = text_formatting(text)
    text = text_config['text']
    base_text = ImageFont.truetype(font_root, text_config['font_size'])

    d = ImageDraw.Draw(blured_image)

    d.text((99, 90), text, font=base_text, fill=(255, 255, 255, 128))

    img = blured_image

    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')

    return img_byte_arr.getvalue()


def sentence_check(text) -> bool:
    """
    Check sentences length
    :param text: text to check
    :return: bool result
    """
    t = text.split()
    for i in t:
        if len(i) > 50:
            return False

    return True


def text_formatting(text) -> dict:
    """
    Format text
    :param text: text string
    :return: dict text, font_size
    """
    t = text.split()
    f_text = []
    buff_text = ''

    for i in t:
        if len(buff_text) < 65:
            buff_text = '%s %s' % (buff_text, i)

        else:
            f_text.append(buff_text)
            buff_text = ''
            buff_text = '%s %s' % (buff_text, i)

        buff_text = buff_text.lstrip().replace('  ', ' ')

    if len(buff_text) != 0:
        f_text.append(buff_text)

    text = "\n".join(f_text)
    return dict(
        text=text,
        font_size=46,
    )


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