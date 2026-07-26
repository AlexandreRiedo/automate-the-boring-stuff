import re


def get_price(sentence: str) -> list[str]:
    return re.findall(r"\$\d+(?:\.\d{2})?", sentence)


print(f"{get_price(input())}")
