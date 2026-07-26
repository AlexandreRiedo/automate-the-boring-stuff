import re
from pathlib import Path

usr_regex = re.escape(input("Enter a regular expression:\n"))
print("-----")
for txt_path in Path.cwd().glob("*.txt"):
    with open(txt_path, "r") as txt_file:
        for line in txt_file:
            if re.search(usr_regex, line):
                print(f"{line.strip()}")
