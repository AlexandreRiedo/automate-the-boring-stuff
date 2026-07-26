import os
import re
import shutil
from pathlib import Path

PATTERN = re.compile(r"spam\d{3}\.txt")
GAPS = {42, 86, 103}
os.chdir(Path.cwd() / "spam")

paths = [
    path
    for path in sorted(Path.iterdir(Path.cwd()), reverse=True)
    if PATTERN.fullmatch(path.name)
]

gap_size = len(GAPS)
for path in paths:
    num = int(path.stem[-3:]) + gap_size
    if num in GAPS:
        gap_size -= 1
        num -= 1
    shutil.move(
        path,
        path.parent / f"{path.stem[:-3]}{num:0>3}{path.suffix}",
    )
