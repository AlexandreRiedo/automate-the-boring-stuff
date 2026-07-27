from pathlib import Path
from string import ascii_uppercase as au


def make_alpha_folders(root_folder):
    root_folder = Path(root_folder).resolve()
    folders = [Path(x) / f"{x}{y}" for x in au for y in au]

    for folder in folders:
        (root_folder / folder).mkdir(parents=True)


make_alpha_folders(Path.cwd())
