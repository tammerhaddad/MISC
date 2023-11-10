from openpyxl import load_workbook
import datetime

# load and activate the sheet
wb = load_workbook("C:\Users\tamme\onedrive\desktop\files\docs\Money2.xlsx")
ws = wb.active

# get the info to add
date = datetime.datetime.now().strftime("%m/%d/%Y")
amount = input("Enter amount: ")
reason = input("Enter reason: ")
details = input("Enter details: ")

# add the info to a new row at the bottom.
ws.append([date, amount, reason, details])

# save
wb.save("pythontestfile.xlsx")