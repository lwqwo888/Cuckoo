#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : send_excel.py
# @Author: handan
# @Date  : 2017/10/8
# @Desc  :

import os

import xlwt
# import sys
# sys.path.append('..')
import os_path


# from public.config import FILE_EXCEL

def send(list_1, file_name):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    try:
        booksheet.write(0, 0, 'track_number')
        booksheet.write(0, 1, 'status')
        # row = ('2045012', '620088260291', '', '未上綫', 'datetime.datetime(2017, 7, 27, 9, 41, 52)',
        #        'datetime.datetime(2017, 7, 27, 14, 2, 12)')
        j = 1
        i = 1
        for x in list_1:
            if not x:
                print '我是空的'
            else:
                booksheet.write(i, 0, str(x[0]))
                booksheet.write(i, 1, x[1])
                i = i + 1
                print str(i)+'nihao'
        PATH = os.path.join(os.path.join(os.path.abspath('.'),), 'karwen')
        # PATH_R = os.path.join(os.path.abspath('.'), 'karwen')
        path_excel = os.path.join(PATH,file_name + '.xls')
        # file_name = os_path.create_folder(PATH, path_excel)
        workbook.save(path_excel)
    except Exception as e:
        print(e)