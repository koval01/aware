from json import loads


def parser(data) -> str:
    """
    Парсер/конвертвер розмітки повідомлення Telegram в HTML
    :param data: JSON-тіло повідомлення
    :return: Оброблене повідомлення
    """
    a = loads(data.text)
    text = a['message']['text']
    plus = 0

    template_select = dict(
        bold='<b>%s</b>',
        italic='<i>%s</i>',
        underline='<u>%s</u>',
        strikethrough='<strike>%s</strike>',
        code='<code>%s</code>',
        text_link='<a href="%s">%s</a>',
        url='<a href="%s">%s</a>',
    )

    for i in a['message']['entities']:
        b_txt = text[i['offset']+plus:i['offset']+i['length']+plus]

        if i['type'] == 'text_link':
            text = "".join((text[:i['offset']+plus], template_select[i['type']] % (i['url'], b_txt), text[i['length']+i['offset']+plus:]))
        elif i['type'] == 'url':
            text = "".join((text[:i['offset']+plus], template_select[i['type']] % (b_txt, b_txt), text[i['length']+i['offset']+plus:]))
        else:
            text = "".join((text[:i['offset']+plus], template_select[i['type']] % b_txt, text[i['length']+i['offset']+plus:]))

        plus += len(template_select[i['type']]) - 2

        if i['type'] == 'text_link':
            plus += len(i['url']) - 2

    return text