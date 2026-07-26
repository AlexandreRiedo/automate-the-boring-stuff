import re

SUB = ("ADJECTIVE", "ADVERB", "NOUN", "VERB")

with open("madLibs.in") as fin:
    text = fin.read()

with open("madLibs.out", "w") as fout:
    out_text = text
    for m in re.finditer(f"\b({'|'.join(SUB)})\b", text):
        usr_input = input(
            f"Enter a{' ' + m.group().lower() if m.group().lower()[0] != 'a' else 'n ' + m.group().lower()}:\n"
        )
        out_text = out_text.replace(m.group(), usr_input, 1)

    """
    CLAUDE CORRECTION, avoids the finditer:
    pattern = re.compile(rf"\b({'|'.join(SUB)})\b")
    out_text = pattern.sub(lambda m: input(f"Enter a{'n' if m.group()[0] in 'AEIOU' else ''} {m.group().lower()}:\n"), text)
    """

    print(out_text)
    fout.write(out_text)
