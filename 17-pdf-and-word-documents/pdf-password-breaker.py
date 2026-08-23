import sys

import pypdf
from rich import print as rprint

pdf = sys.argv[1]

with open("dictionary.txt", "r") as fin:
    words = (w for s in map(str.strip, fin) for w in (s.lower(), s.upper()))
    reader = pypdf.PdfReader(pdf)
    for word in words:
        rprint(f"[cyan]Attempting decryption with {word}")
        if reader.decrypt(word) != pypdf.PasswordType.NOT_DECRYPTED:
            writer = pypdf.PdfWriter(reader)
            with open(f"{pdf.removesuffix('.pdf')}_decrypted.pdf", "wb") as fout:
                writer.write(fout)
                rprint(f"\n[green]Decrypted [blue]{pdf} with password [purple]{word}")
            break
