import openpyxl

from config.config import EXCEL_NAME, EXCEL_SHEET_1


def read_excel():
    workbook = openpyxl.load_workbook(EXCEL_NAME)
    sheet = workbook[EXCEL_SHEET_1  ]
    data = []
    key = [cell.value for cell in sheet[2]]
    for row in sheet.iter_rows(min_row=3, values_only=True):
        data.append(dict(zip(key, row)))
    return data

