import re


def re_strip(a: str, rm: str | None = None) -> str:
    chars_set = r"\s" if rm is None else f"[{re.escape(rm)}]"
    a = re.sub(f"^{chars_set}+", "", a)
    a = re.sub(f"{chars_set}+$", "", a)
    return a


print(re_strip("1111    abcd1111    x", "1111  xxy  "))
print(re_strip(" awdkald wad kawd lakw dka              "))
print(re_strip("---hia-", "a-z"))
