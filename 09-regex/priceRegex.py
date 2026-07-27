import re

from rich import print as rprint


def get_price(sentence: str) -> list[str]:
    return re.findall(r"\$\d+(?:\.\d{2})?", sentence)


rprint(f"{get_price(input())}")
