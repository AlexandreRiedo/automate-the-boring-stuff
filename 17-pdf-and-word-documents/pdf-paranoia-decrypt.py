import os
import sys
from pathlib import Path

import pypdf
from pypdf.errors import PdfReadError, WrongPasswordError
from rich import print as rprint

password = " ".join(sys.argv[1:])

for root, dirs, files in os.walk(Path.cwd()):
    for pdf in [(Path(root) / f) for f in files if Path(f).suffix == ".pdf"]:
        try:
            if (reader := pypdf.PdfReader(pdf)).is_encrypted:
                # Decrypt the PDF
                reader.decrypt(password)

                # Create a decrypted copy
                writer = pypdf.PdfWriter(clone_from=reader)
                copy = pdf.parent / f"{pdf.stem.removesuffix('_encrypted')}.pdf"
                if copy == pdf:
                    copy = pdf.parent / f"{pdf.stem}_decrypted.pdf"
                with open(copy, "wb") as file:
                    writer.write(file)
                    rprint(f"[green]Decryption successful for: [blue]{pdf}")
        except (OSError, ValueError, PdfReadError, WrongPasswordError) as e:
            rprint(f"[red]Error for {pdf}: [blue]{e}")
