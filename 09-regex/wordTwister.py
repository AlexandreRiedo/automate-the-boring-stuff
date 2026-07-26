import re

pattern = re.compile(r"(\b\w+)(\w\b)")
ans = pattern.sub(r"\2\1", "Hello world! How are you? I am fine.")
assert ans == "oHell dworl! wHo ear uyo? I ma efin."
