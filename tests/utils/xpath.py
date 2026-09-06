"""Сборка XPath по видимому тексту.

Текст может содержать кавычки, поэтому одинарные и двойные разбираются
отдельно, а смешанный случай собирается через `concat`.
"""


def by_text(text: str, tag: str = "*") -> str:
    if "'" not in text:
        return f"//{tag}[normalize-space()='{text}']"
    if '"' not in text:
        return f'//{tag}[normalize-space()="{text}"]'

    chunks: list[str] = []
    parts = text.split("'")
    for index, part in enumerate(parts):
        if part:
            chunks.append(f"'{part}'")
        if index != len(parts) - 1:
            chunks.append('"\'"')
    return f"//{tag}[normalize-space()=concat({', '.join(chunks)})]"


def contains_text(text: str, tag: str = "*") -> str:
    quoted = f'"{text}"' if "'" in text else f"'{text}'"
    return f"//{tag}[contains(normalize-space(), {quoted})]"
