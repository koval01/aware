from .response_methods import *
from types import SimpleNamespace
from json import loads
from .formatting_parser import parser as telegram_message_entities_parser
import logging

logger = logging.getLogger(__name__)


def language(code):
    if code != 'ru' or code != 'uk':
        return 'en'
    return code


class heart:
    def __init__(self, message, token):
        self.message = loads(message.replace('from', 'from_user'), object_hook=lambda x: SimpleNamespace(**x)).message
        self.msg = Message(token)
        self.bot = Bot(token)

    try:
        def start(self):
            try:
                if ['/start'] in self.message.text:
                    m = dict(
                        uk='Привіт! Моє ім\'я %s. Надішли мені текст (підтримується форматування і посилання) і я відправлю його на перевірку.',
                        ru='Привет! Мое имя %s. Пришли мне текст (поддерживается форматирование и ссылки) и я отправлю его на проверку.',
                        en='Hi there! My name is %s. Send me the text (formatting and links are supported) and I will send it for review.',
                    )
                    ln = language(self.message.from_user.language_code)
                    self.msg.send_message(
                        self.message.chat.id,
                        m[ln] % self.bot.first_name
                    )
            except Exception as e:
                logger.error("start: %s" % e)

        def text(self):
            try:
                print(self.message.text)
            except Exception as e:
                logger.debug("text: %s" % e)

    except Exception as e:
        logger.warning("heart: %s" % e)