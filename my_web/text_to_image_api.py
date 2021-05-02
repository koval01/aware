from PIL import Image, ImageFilter, ImageDraw, ImageFont
from io import BytesIO
from requests import get
from django.conf import settings
import logging, os

logger = logging.getLogger(__name__)
base_dir = settings.BASE_DIR
font_root_Roboto = os.path.join(base_dir, 'my_web/fonts_for_Pillow/Roboto-Light.ttf')
font_root_Quicksand = os.path.join(base_dir, 'my_web/fonts_for_Pillow/Quicksand-Medium.ttf')


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


def image_edit(image, text, author) -> bytes:
    """
    Prepare an image using Pillow library
    :param image: image to edit
    :param text: The text you want to overlay on the image
    :param author: Author photo
    :return: the finished image, which is also translated into raw
    """
    img = Image.open(BytesIO(image))

    blured_image = img.filter(ImageFilter.GaussianBlur(15))
    text = text_formatting(text)
    author = '— %s' % author
    base_text = ImageFont.truetype(font_root_Roboto, 46)
    author_font = ImageFont.truetype(font_root_Roboto, 38)
    water_font = ImageFont.truetype(font_root_Quicksand, 70)

    d = ImageDraw.Draw(blured_image)

    d.text((99, 90), text, font=base_text, fill=(255, 255, 255, 128))
    d.text((99, 830), author, font=author_font, fill=(255, 255, 255, 128), align='left')
    d.text((1325, 800), 'awse.us', font=water_font, fill=(255, 255, 255, 128))

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


def text_formatting(text) -> str:
    """
    Format text
    :param text: text string
    :return: edited text string
    """
    t = text.split()
    f_text = []
    buff_text = ''

    for i in t:
        if len(buff_text) < 51:
            buff_text = '%s %s' % (buff_text, i)

        else:
            f_text.append(buff_text)
            buff_text = ''
            buff_text = '%s %s' % (buff_text, i)

        buff_text = buff_text.lstrip().replace('  ', ' ')

    if len(buff_text) != 0:
        f_text.append(buff_text)

    return "\n".join(f_text)


def percent(percent_value, whole):
    """
    Function for easy calculation of interest
    :param percent_value: Percents
    :param whole: Basic number
    :return: Percentage result
    """
    return whole/((1-percent_value)*100)*100


def get_result(text, author) -> dict:
    """
    Request image processing
    :param text: The text you want to overlay on the image
    :param author: Author photo
    :return: The finished image in raw
    """
    img = get_image()
    result = image_edit(img['img'], text, author)
    return dict(
        img=result,
        status_code=img['status_code'],
        reason=img['reason'],
        headers=img['headers'],
    )