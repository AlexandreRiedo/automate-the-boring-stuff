import re
import zipfile


def extract_in_folder(zip_filename, folder):
    with zipfile.ZipFile(zip_filename) as zf:
        re_pattern = re.compile(rf"\b{folder}/")
        for filename in (x for x in zf.namelist() if re.search(re_pattern, x)):
            zf.extract(filename)


extract_in_folder("eggs.zip", "spam")
