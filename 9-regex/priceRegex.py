import re


def get_price(sentence: str) -> list[str]:
    return re.findall(r"\$\d+(?:.\d{2,})?", sentence)


print(get_price(input()))
