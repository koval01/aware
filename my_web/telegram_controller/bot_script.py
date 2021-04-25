from .response_methods import Message
from types import SimpleNamespace
from json import loads


def heart(message):
    message = loads(message, object_hook=lambda x: SimpleNamespace(**x)).message
    print(message)
    print(message.text)
    print(message.chat.id)
    if message.text:
        Message.send_message(message.chat.id, 'Ты отправил мне текст: %s' % message.text)
    else:
        Message.send_message(message.chat.id, 'Это видь не текст? Верно?')