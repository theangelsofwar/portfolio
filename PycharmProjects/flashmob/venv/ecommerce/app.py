import openpyexcel as excel
from openpyexcel.chart import BarChart, Reference

def process_workbook(filename):

    wb=excel.load_workbook(filename)
    sheet=wb['Sheet 1']

    for row in range(, sheet.max_row+1)
        print(row)

        sheet.cell(row,3)
        corected_price=cell.value*.9
        correct_price_cell=sheet.cell(row,4)
        correct_price_cell.value=corrected_price


    values=Reference(sheet,
              min_row=2,
              max_row=sheet.max_row,
              min_col=4,
              max_col=4)

    chart=BarChart()
    chart.add_data(values)
    sheet.add_chart(chart,'e2')

    wb.save(filename)