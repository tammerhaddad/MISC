from openpyxl import load_workbook
import datetime

# FOR logging costs when i was in london 2022-23

# load and activate the sheet
path = r"C:\Users\tamme\onedrive\desktop\files\docs\Money.xlsx"
wb = load_workbook(path)
ws = wb.active

# get the info to add
date = datetime.datetime.now().strftime("%m/%d/%Y")
amount, reason, details = map(input, ["Enter amount: ", "Enter reason: ", "Enter details: "])

# add the info to a new row at the bottom.
ws.append([date, float(amount), reason, details])

# save
wb.save(path)