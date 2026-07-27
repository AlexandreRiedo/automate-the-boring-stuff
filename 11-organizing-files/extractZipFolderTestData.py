import zipfile
from pathlib import Path

EGGS = Path.cwd() / "eggs.zip"

# The layout from the exercise: extract_in_folder('eggs.zip', 'spam') must pull
# out data2.txt and data3.txt only.
FILES = [
    "data1.txt",
    "spam/data2.txt",
    "spam/data3.txt",
    "bacon/data4.txt",
]

# Folder names that merely start with 'spam': these must stay in the archive.
DECOYS = [
    "spammy/data5.txt",
    "spam-old/data6.txt",
]

with zipfile.ZipFile(EGGS, "w") as eggsZip:
    for name in FILES + DECOYS:
        eggsZip.writestr(name, f"original path: {name}\n")
