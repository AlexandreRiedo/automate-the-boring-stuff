import os
import sys
from pathlib import Path

import pypdf
from pypdf.errors import PdfReadError
from rich import print as rprint

password = " ".join(sys.argv[1:])

for root, dirs, files in os.walk(Path.cwd()):
    for pdf_filename in [Path(root) / f for f in files if Path(f).suffix == ".pdf"]:
        pdf_encrypted_filename = Path(root) / f"{pdf_filename.stem}_encrypted.pdf"

        try:
            writer = pypdf.PdfWriter(clone_from=pypdf.PdfReader(pdf_filename))
            writer.encrypt(password, algorithm="AES-256")

            with open(pdf_encrypted_filename, "wb") as file:
                writer.write(file)
                rprint(f"[green]Wrote: [blue]{pdf_encrypted_filename}\n")
        except (OSError, ValueError, PdfReadError) as e:
            rprint(f"[red]Error [blue]{pdf_encrypted_filename} with [green]{e}\n")
