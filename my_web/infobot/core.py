from requests_cache import CachedSession


session = CachedSession('infobot_cache')
TOKEN = '1750936339:AAFnvBV1fkUyxoXhAT0fsI0jxf9A6S1ps4M'
HOST = f'https://api.telegram.org/bot{TOKEN}/SendMessage'
admins = [
    '542956255',
    '652933710',
]


def send_data(user_agent, ip_address, link_or_search, type_data) -> bool:
    """
    Send message to admins
    :param user_agent: User agent request
    :param ip_address: IP address request
    :param link_or_search: Redirect link or search text
    :param type_data: Log type
    :return: Bool result request to Telegram API
    """
    text_message = 'USER AGENT: <code>%s</code>\nIP ADDRESS: <code>%s</code>' \
                   '\n%s: <code>%s</code>' % (
                        user_agent, ip_address, type_data.upper(), link_or_search,
                    )
    for admin_chat_id in admins:
        request = session.get(
            HOST, params={
                'chat_id': admin_chat_id,
                'text': text_message,
                'parse_mode': 'HTML',
            }
        )
        if request.status_code == 200:
            yield True