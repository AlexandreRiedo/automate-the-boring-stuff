import re


def is_pwd_strong(pwd: str, patterns: list[str]) -> bool:
    return all(re.search(p, pwd) for p in patterns) and len(pwd) >= 8


PATTERNS = [r"[a-z]", r"[A-Z]", r"[0-9]"]
test = input()
print(f"Is your password ({test}) strong enough? It's {is_pwd_strong(test, PATTERNS)}.")
