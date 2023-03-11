def encoder(*args: str) -> str:
    """ Функція для кодування callback_data в str """
    return "&&".join(args)


def decoder(text: str) -> list:
    """ Функція для декодування str в список значень """
    return text.split('&&')


def card_formated(card_number: str) -> str:
    """ Функція для форматування номерів кард, типу: "1234 1234 1234 1234" """
    if len(card_number) == 16:
        card_number = f'{card_number[:4]} {card_number[4:8]} {card_number[8:-4]} {card_number[12:]}'

    return card_number
