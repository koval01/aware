from time import time
import logging, requests_cache, regex

logger = logging.getLogger(__name__)
session = requests_cache.CachedSession('deepl_get')


def translate_text(text, lang=None, lang_to='EN') -> str:
    """
    Translate text
    :param text: text string
    :param lang: original lang (optional)
    :param lang_to: exit text
    :return: translated text
    """
    for _ in range(2):
        if not lang:
            lang = "auto"
        data = session.post(
            'https://www2.deepl.com/jsonrpc',
            headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4484.3 Safari/537.36",
            },
            json={
                "jsonrpc": "2.0",
                "method": "LMT_handle_jobs",
                "params": {
                    "jobs": [
                        {
                            "kind": "default",
                            "raw_en_sentence": str(text),
                            "raw_en_context_before": [
                            ],
                            "raw_en_context_after": [
                            ],
                            "preferred_num_beams": 4,
                            "quality": "fast"
                        }
                    ],
                    "lang": {
                        "user_preferred_langs": [
                            "DE",
                            "RU",
                            "EN"
                        ],
                        "source_lang_user_selected": lang,
                        "target_lang": lang_to
                    },
                    "priority": -1,
                    "commonJobParams": {
                    },
                    "timestamp": int(str(time()).replace('.', '')[:13])
                },
                "id": 0
            }
        ).json()['result']['translations'][0]['beams'][0]['postprocessed_sentence']
        return data


def latin_detect(text) -> str:
    """
    Detect latin text and translate
    :param text: text string
    :return: translated text (to russian)
    """
    result = regex.sub(r'[^.,-!?:;\p{Latin}]', '', text)
    return translate_text(result, lang_to="RU")


def cyrillic_detect(text) -> str:
    """
    Detect cyrillic text and translate
    :param text: text string
    :return: translated text (to english)
    """
    result = regex.sub(r'[^.,-!?:;\p{Cyrillic}]', '', text)
    return translate_text(result)


def translate_simple(text) -> str:
    """
    Auto translate detect function
    :param text: text string
    :return: result (String)
    """
    try:
        return translate_text(text, lang_to="RU")
    except Exception as e:
        logger.warning(e)
