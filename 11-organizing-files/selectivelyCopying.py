import os
import shutil
from pathlib import Path

root = Path.cwd() / ".."
paste_folder = Path.cwd() / "selectivelyCopying"

for folder_name, subfolders, filenames in os.walk(root):
    for filename in filenames[:10]:
        if (filepath := (Path(folder_name) / filename)).suffix == ".py":
            shutil.copy(filepath, paste_folder)
