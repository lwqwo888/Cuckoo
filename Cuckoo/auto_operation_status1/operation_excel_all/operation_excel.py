#!/usr/bin/env python
# -*- coding: utf-8 -*-
# xlrd是读excel，xlwt是写excel的库
import xlrd
# data = xlrd.open_workbook('C:\Users\Administrator\Desktop\Logistics crawl scrip\caozuo.xls')
# tables = data.sheets()[0]
#
# print tables.nrows
# print tables.cell_value(3,3)

class OperationExcel(object):
     def __init__(self,file_name=None,sheet_id=None):
         if file_name:
             self.file_name = file_name
             self.sheet_id  = sheet_id
             # 还有这种操作?
             self.data = self.get_data()
         else:
              self.file_name = '../need_operation_excel/2.xlsx'
              self.sheet_id  = 0
         self.data = self.get_data()

     # 获取sheets的内容
     def get_data(self):
         # 打开excal文件
         data = xlrd.open_workbook(self.file_name)
         # 获得指定页签对象,默认为0第一页
         tables = data.sheets()[self.sheet_id]
         return tables
     def A(self):
         print '我是父类'

     # 获取单元格的行数
     def get_line(self):
         tables = self.data
         return tables.nrows

     # 获取某个单元格的内容
     def get_cell_value(self,row,col):
         return self.data.cell_value(row,col)

     # 获取一整行的数据
     def get_row_all_data(self,row_number):
         tables = self.data
         return tables.row_values(row_number)

     # 获取一整列的数据
     # 如果你在col_values又多加了两个参数，就可以选择，这一列具体的多少行-》多少行的数据
     #
     def get_col_all_data(self, col_number):
         # print self.file
         tables = self.data
         return tables.col_values(col_number,start_rowx=1,end_rowx=45188)


if __name__ == "__main__":
     opers =  OperationExcel()
     opers.get_line()
     opers.get_cell_value(3,3)
     print opers.get_col_all_data(0)


