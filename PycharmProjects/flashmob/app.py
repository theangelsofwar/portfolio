import openpyexcel as excel
wb=excel.load_workbook('transactions.xlsx')
sheet=wb['Sheet 1']
cell=sheet['a1']
sheet.cell(1,1)
print(sheet.max_row)