import pdfminer.high_level
import pypdf
from pypdf.errors import PyPdfError

PDF_FILENAME = "../book-materials/Recursion_Chapter1.pdf"
TEXT_FILENAME = "recursion.txt"


def extract(path):
    try:
        reader = pypdf.PdfReader(path)
        parts = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(parts)
        if text.strip():  # Check if pypdf didn't return a blank string
            return text
    except (PyPdfError, ValueError, KeyError, RecursionError) as err:
        print(f"pypdf failed ({err}), falling back to pdfminer")
    return pdfminer.high_level.extract_text(path)  # Quite powerful


with open(TEXT_FILENAME, "w", encoding="utf-8") as file_obj:
    file_obj.write(extract(PDF_FILENAME))
