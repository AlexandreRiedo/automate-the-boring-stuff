import os
import re
import shutil
from pathlib import Path

os.chdir("dates")
PATTERN = re.compile(r"(?<!\d)(\d{2})-(\d{2})-(\d{4})(?!\d)")

for foldername, subfolders, filenames in os.walk(Path.cwd()):
    for filename in filenames:
        if PATTERN.search(filename):
            new_filename = re.sub(PATTERN, r"\2-\1-\3", filename)
            shutil.move(Path(foldername) / filename, Path(foldername) / new_filename)
