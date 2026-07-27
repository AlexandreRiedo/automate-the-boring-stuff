import os
from collections import defaultdict
from pathlib import Path

from rich import print as rprint


def find_dup_filenames(folder):
    findings = defaultdict(list)
    for foldername, _, filenames in os.walk(Path(folder).resolve()):
        for filename in filenames:
            findings[filename].append(Path(foldername) / filename)

    return {k: v for k, v in findings.items() if len(v) >= 2}


ans = find_dup_filenames(Path.cwd())
for filename in sorted(ans):
    rprint(f"[blue]{filename}")
    for path in sorted(ans[filename]):
        rprint(f"    [green]{path}")
