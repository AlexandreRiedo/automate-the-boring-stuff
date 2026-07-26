import os
import re
import shutil
from pathlib import Path

root = Path.cwd() / ".."
paste_dir = Path.cwd() / "selectivelyCopying"
if paste_dir.is_dir():
    shutil.rmtree(paste_dir)
paste_dir.mkdir()

for folder_name, subfolders, filenames in os.walk(root):
    subfolders[:] = [
        d for d in subfolders if (Path(folder_name) / d).resolve() != paste_dir
    ]  # Claude's Correction
    for filename in filenames:
        if (filepath := (Path(folder_name) / filename)).suffix == ".py":
            while filename in {x.name for x in paste_dir.iterdir()}:
                if num := re.search(rf"(\d+){re.escape(filepath.suffix)}$", filename):
                    num = int(num.group(1)) + 1
                    filename = f"{filepath.stem}{num}{filepath.suffix}"
                else:
                    filename = f"{filepath.stem}{1}{filepath.suffix}"

            shutil.copy(filepath, paste_dir / filename)
