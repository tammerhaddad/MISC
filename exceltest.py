from openpyxl import Workbook
import os
import datetime
import os
from openpyxl import load_workbook

os.chdir(r"C:\Users\tamme\onedrive\desktop\files\docs")

# open the file pythontestfile.xlsx instead of the workbook, so i can edit
wb = load_workbook("pythontestfile.xlsx")
ws = wb.active

# open the folder

date = datetime.datetime.now().strftime("%m/%d/%Y")
amount = input("Enter amount: ")
reason = input("Enter reason: ")
details = input("Enter details: ")
ws.append([date, amount, reason, details])
# Python types will automatically be converted
wb.save("pythontestfile.xlsx")