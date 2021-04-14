from random import choice


def get_text() -> str:
    """
    Random text load button
    :return: text
    """
    list_text = [
        'Загрузка',
        'Loading',
        'Bezig met laden',
        'Завантаження',
        '로딩 중',
        'Barkirin',
        'တင်နေသည်',
        'Đang tải',
        'Hoʻouka nei',
        '載入中',
        '読み込み中',
        'Caricamento in corso',
        'Luede',
        'Ładowanie',
        'Betöltés',
        'Ачаалж байна',
        'Načítava',
        'Φόρτωση',
        'Įkeliama',
    ]
    return choice(list_text)+'...'