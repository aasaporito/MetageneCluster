import xlwt
from xlwt import Workbook

def wtExcell(names,fileName): 
    wb = Workbook()
    sheet1= wb.add_sheet('Sheet 1')
    for i,cluster in enumerate(names): 
        sheet1.write(0,i, 'Cluster '+str(i))
        for j,name in enumerate(cluster):
            sheet1.write(j+1,i,name)
    
    wb.save(fileName+'.xls')


