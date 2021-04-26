from .response_methods import Message
from types import SimpleNamespace
from json import loads
import logging

logger = logging.getLogger(__name__)

def heart(message, token):
    bot = Message(token)
    message = loads(message, object_hook=lambda x: SimpleNamespace(**x)).message
    try:
        if message.text:
            bot.send_message(message.chat.id, 'Ты отправил мне текст: %s' % message.text)
    except Exception as e:
        bot.send_message(message.chat.id, 'Случилась ошибка: %s' % e)