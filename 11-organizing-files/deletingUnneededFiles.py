import os
from operator import itemgetter
from pathlib import Path

from rich import print as rprint

SIZE = 104_857_600
out = []

for foldername, subfolders, filenames in os.walk(Path.cwd()):
    for filename in filenames:
        filepath = Path(foldername) / filename
        if (file_size := os.path.getsize(filepath)) > SIZE:
            out.append((f"{filepath=}", file_size))

    folder_size = 0
    for exp_foldername, _, exp_filenames in os.walk(foldername):
        for exp_filename in exp_filenames:
            exp_filepath = Path(exp_foldername) / exp_filename
            folder_size += os.path.getsize(exp_filepath)
    if folder_size > SIZE:
        out.append((f"{foldername=}", folder_size))


for line, size in sorted(out, key=itemgetter(1), reverse=True):
    rprint(line, f"{(size / 1024**2):.2f} MB")
