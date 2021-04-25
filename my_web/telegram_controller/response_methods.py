from requests import get
from .config import *


class Message:
    @staticmethod
    def send_message(
            chat_id, text,
            parse_mode=None, entities=None,
            disable_web_page_preview=None, disable_notification=None,
            reply_to_message_id=None, allow_sending_without_reply=None,
            reply_markup=None,
    ) -> bool:
        """
        Send message to user
        :param chat_id: chat id
        :param text: message text
        :param parse_mode: parse mode (Html or Markdown)
        :param entities: entities message
        :param disable_web_page_preview: disable telegram preview web page
        :param disable_notification: disable notify receive message users
        :param reply_to_message_id: reply to message by id message
        :param allow_sending_without_reply: if the message should be sent even if the specified replied-to message is not found
        :param reply_markup: reply button by message or keyboard
        :return: bool result
        """
        method = 'sendMessage'
        a = get(f"{API_HOST}{TOKEN}{method}", params={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "entities": entities,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "allow_sending_without_reply": allow_sending_without_reply,
            "reply_markup": reply_markup
        })
        print(a.url)
        if a.status_code == 200:
            return True