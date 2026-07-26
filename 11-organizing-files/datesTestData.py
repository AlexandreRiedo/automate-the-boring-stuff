import shutil
from pathlib import Path

DATES = Path.cwd() / "dates"

# Filenames holding an MM-DD-YYYY date: these must be renamed to DD-MM-YYYY.
MATCHES = [
    "spam12-31-1900.txt",
    "invoice01-05-2020.txt",
    "report11-02-1999.pdf",
    "vacation-photo07-04-2021.jpg",
    "09-15-2015.txt",
    "sub1/memo03-14-1592.txt",
    "sub1/meeting10-08-2018.docx",
    "sub1/sub1a/taxes04-15-2022.pdf",
    "sub1/sub1a/backup12-25-2001.zip",
    "sub2/holiday-list06-30-2010.txt",
    "sub2/01-01-2000.log",
    "05-05-2005/inside09-09-2009.txt",  # the folder name must stay untouched
]

# Filenames that only look like they hold a date: these must stay untouched.
DECOYS = [
    "notadate.txt",
    "budget2020.txt",
    "release12-31-19.txt",  # two-digit year
    "logs1-5-2020.txt",  # single-digit month and day
    "archive123-31-1900.txt",  # extra digit before the month
    "sub1/README.md",
    "sub2/empty-notes.txt",
]

shutil.rmtree(DATES, ignore_errors=True)
for name in MATCHES + DECOYS:
    path = DATES / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"original name: {path.name}\n")
