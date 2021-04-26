from .response_methods import *
from types import SimpleNamespace
from json import loads
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
                        uk='Привіт! Моє ім\'я %s. Я можу тобі допомогти у пошуку інформації.',
                        ru='Привет! Мое имя %s. Я могу тебе помочь в поиске информации.',
                        en='Hi there! My name is %s. I can help you find information.',
                    )
                    ln = language(self.message.from_user.language_code)
                    self.msg.send_message(
                        self.message.chat.id,
                        m[ln] % self.bot.first_name
                    )
            except Exception as e:
                logger.error("start: %s" % e)

        def help_(self):
            try:
                if ['/help'] in self.message.text:
                    pass
            except Exception as e:
                logger.debug("help_: %s" % e)

    except Exception as e:
        logger.warning("heart: %s" % e)