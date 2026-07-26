import os
import re
from pathlib import Path

PATTERN = re.compile(r"spam\d{3}\.txt")

os.chdir(Path.cwd() / "spam")

gap = 0
for idx, path in enumerate(
    [path for path in sorted(Path.iterdir(Path.cwd())) if PATTERN.fullmatch(path.name)],
    1,
):
    if int(path.stem[-3:]) - gap != idx:
        print("Gap Found!")
        gap += int(path.stem[-3:]) - gap - idx
    Path.rename(
        path,
        path.parent / f"{path.stem[:-3]}{int(path.stem[-3:]) - gap:0>3}{path.suffix}",
    )
