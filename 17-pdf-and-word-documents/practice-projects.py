import os
from pathlib import Path

import pypdf
from pypdf.errors import PyPdfError
from rich import print as rprint


def pdf_word_count(pdf_filename: str) -> int:
    count = 0
    reader = pypdf.PdfReader(pdf_filename)
    for page in reader.pages:
        count += len(page.extract_text().split())

    return count


def pdf_word_count_CORRECTION(pdf_filename):
    reader = pypdf.PdfReader(pdf_filename)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return len(text.split())


rprint("[bright_blue]----- PDF Document Word Counter -----")
rprint(f"{pdf_word_count("more-pdfs/ATBSWP-chapter-9.pdf")=}")
rprint(f"[red]{pdf_word_count_CORRECTION("more-pdfs/ATBSWP-chapter-9.pdf")=}")
rprint(f"{pdf_word_count("more-pdfs/AWTLCL-21.10.pdf")=}")
rprint(f"[red]{pdf_word_count_CORRECTION("more-pdfs/AWTLCL-21.10.pdf")=}")
rprint("\n")


def search_all_PDFs(text: str, folder=".", case_sensitive=False) -> list[str]:
    found = []
    for root, _, files in os.walk(folder):
        for pdf in (f for f in files if f.endswith(".pdf")):
            try:
                reader = pypdf.PdfReader(Path(root) / pdf)
                for page_number, page in enumerate(reader.pages, 1):
                    for word in page.extract_text().split():
                        if not case_sensitive and text.lower() in word.lower():
                            found.append(f"In {pdf} on page {page_number}")
                            break
                        if case_sensitive and text in word:
                            found.append(f"In {pdf} on page {page_number}")
                            break
            except (OSError, ValueError, PyPdfError) as e:
                rprint(f"[magenta1]Error encountered on {Path(root) / pdf}: {e}")
    return found


def search_all_PDFs_CORRECTION(text, folder=".", case_sensitive=False):
    matches = []
    for filename in os.listdir(folder):
        if not filename.lower().endswith(".pdf"):
            # Skip non-PDF files:
            continue
        reader = pypdf.PdfReader(Path(folder) / filename)
        for page_number, page_obj in enumerate(reader.pages):
            page_text = page_obj.extract_text()
            if (
                not case_sensitive
                and text.lower() in page_text.lower()
                or case_sensitive
                and text in page_text
            ):
                matches.append(f"In {filename} on page {page_number}")
    return matches


rprint("[bright_blue]----- Searching All PDFs in a Folder -----")
rprint("\n".join(search_all_PDFs_CORRECTION("python", "more-pdfs")))
rprint("")
rprint("\n".join(search_all_PDFs("python", "more-pdfs")))
rprint("")
