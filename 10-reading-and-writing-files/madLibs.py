import re

SUB = ("ADJECTIVE", "ADVERB", "NOUN", "VERB")

with open("madLibs.in") as fin:
    text = fin.read()

with open("madLibs.out", "w") as fout:
    out_text = text
    for m in re.finditer(f"({'|'.join([x for x in SUB])})", text):
        usr_input = input(
            f"Enter a{' ' + m.group().lower() if m.group().lower()[0] != 'a' else 'n ' + m.group().lower()}:\n"
        )
        out_text = out_text.replace(m.group(), usr_input, 1)

    print(out_text)
    fout.write(out_text)
