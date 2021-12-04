from random import choice
from string import ascii_letters, digits


def make_random_string(length: int, chars: str = None) -> str:
    """Возвращает строку из случайных символов chars длиной length.

    Если chars не передан, значением будет строка из цифр и букв ASCII.
    Отрицательное целое число для length вернёт пустую строку.
    """

    if chars is None:
        chars = f"{ascii_letters}{digits}"

    return "".join(choice(chars) for _ in range(length))
