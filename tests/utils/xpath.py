"""Сборка XPath по видимому тексту.

Текст приходит с экрана и может содержать кавычки любого вида, а экранировать
их XPath 1.0 не умеет. Поэтому текст сначала превращается в литерал, и только
готовый литерал подставляется в выражение.
"""

SINGLE = "'"
DOUBLE = '"'


def as_literal(text: str) -> str:
    """Обернуть произвольную строку в XPath-литерал.

    Пока в строке нет одинарной кавычки, хватает обычных апострофов. Если она
    есть, но нет двойной — берём двойные. Если есть обе, строка режется по
    одинарной кавычке, куски заворачиваются в апострофы (одинарных внутри уже
    нет) и склеиваются через `concat` с отдельным символом кавычки.
    """
    if SINGLE not in text:
        return f"{SINGLE}{text}{SINGLE}"
    if DOUBLE not in text:
        return f"{DOUBLE}{text}{DOUBLE}"

    parts: list[str] = []
    for index, piece in enumerate(text.split(SINGLE)):
        if index:
            parts.append(f'{DOUBLE}{SINGLE}{DOUBLE}')
        if piece:
            parts.append(f"{SINGLE}{piece}{SINGLE}")
    return f"concat({', '.join(parts)})"


def by_text(text: str, tag: str = "*") -> str:
    """Элемент, весь видимый текст которого равен заданному."""
    return f"//{tag}[normalize-space()={as_literal(text)}]"


def contains_text(text: str, tag: str = "*") -> str:
    """Элемент, в видимом тексте которого встречается заданный кусок."""
    return f"//{tag}[contains(normalize-space(), {as_literal(text)})]"
