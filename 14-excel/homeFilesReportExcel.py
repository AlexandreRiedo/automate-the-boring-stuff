import os
from operator import itemgetter
from pathlib import Path

import openpyxl
import openpyxl.styles


def get_home_folder_size() -> list[tuple[str, float]]:
    h = Path.home()
    sizes = []
    for folder_name, _, filenames in os.walk(h):
        for filename in filenames:
            try:
                size = round((Path(folder_name) / filename).stat().st_size / 1024**2, 2)
                sizes.append((filename, size))
            except OSError as e:
                print(f"{e}")
    sizes.sort(key=itemgetter(1), reverse=True)
    return sizes


def make_excel_report(fns: list[tuple[str, float]]):
    wb = openpyxl.Workbook()
    sheet = wb[wb.sheetnames[0]]

    sheet.title = "File Sizes (Megabytes)"
    sheet.column_dimensions["A"].width = 50
    sheet.column_dimensions["B"].width = 25

    font_headers = openpyxl.styles.Font(name="Aptos", bold=True)
    sheet["A1"] = "fileName"
    sheet["A1"].font = font_headers
    sheet["B1"] = "sizeMegabytes"
    sheet["B1"].font = font_headers

    for row_idx, (name, size) in enumerate(fns, 2):
        sheet[f"A{row_idx}"] = name
        sheet[f"B{row_idx}"] = size
    wb.save("homeFilesReport.xlsx")


make_excel_report(get_home_folder_size())
