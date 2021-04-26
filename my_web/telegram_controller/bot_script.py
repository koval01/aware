from .response_methods import Message
from types import SimpleNamespace
from json import loads
import logging

logger = logging.getLogger(__name__)

def heart(message):
    message = loads(message, object_hook=lambda x: SimpleNamespace(**x)).message
    try:
        if message.text:
            Message.send_message(message.chat.id, 'Ты отправил мне текст: %s' % message.text)
        else:
            Message.send_message(message.chat.id, 'Это видь не текст? Верно?')
    except Exception as e:
        logger.warning(e)