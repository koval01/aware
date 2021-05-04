from requests_cache import CachedSession
from time import time


session = CachedSession('infobot_cache')
TOKEN = '1696588778:AAHlQf34MS54HP9QU9O6JIK8Lw-YBuqxs3Y'
HOST = f'https://api.telegram.org/bot{TOKEN}/SendMessage'
admins = [
    '542956255',
    '652933710',
]


def send_data(user_agent, ip_address, link_or_search, type_data,
              user_request_method, user_referer) -> bool:
    """
    Send message to admins
    :param user_agent: User agent request
    :param ip_address: IP address request
    :param link_or_search: Redirect link or search text
    :param type_data: Log type
    :param user_request_method: Request method
    :param user_referer: User referer
    :return: Bool result request to Telegram API
    """
    text_message = 'UNIX TIME: <code>%s</code>\nUSER AGENT: <code>%s</code>\nIP ADDRESS: <code>%s</code>' \
                   '\n%s: <code>%s</code>\nREQUEST METHOD: <code>%s</code>\nREFERER: <code>%s</code>' % (
                        time(), user_agent, ip_address, type_data.upper(), link_or_search,
                        user_request_method.upper(), user_referer,
                    )
    for admin_chat_id in admins:
        result = False
        request = session.get(
            HOST, params={
                'chat_id': admin_chat_id,
                'text': text_message,
                'parse_mode': 'HTML',
            }
        )
        if request.status_code == 200:
            result = True
    return result