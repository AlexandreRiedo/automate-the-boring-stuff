import re


def laugh_score(laugh: str) -> int:
    if m := re.search("ha[ah]*", laugh, re.IGNORECASE):
        return len(m.group())
    return 0


assert laugh_score("abcdefg") == 0
assert laugh_score("h") == 0
assert laugh_score("ha") == 2
assert laugh_score("HA") == 2
assert laugh_score("hahaha") == 6
assert laugh_score("ha ha ha") == 2
assert laugh_score("haaaaa") == 6
assert laugh_score("ahaha") == 4
assert laugh_score("Harry said Hahaha") == 2
