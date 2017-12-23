#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : data.py
# @Author: handan
# @Date  : 2017/11/30
# @Desc  :

############################################################
# 此脚本属于批量操作excel，学会使用它让你的工作效率极大的提升come on #
############################################################
import urllib2
# import sys
# sys.path.append('../')
from lxml import etree

from operation_excel import OperationExcel
from config import FILE_NAME, col_number, FILE_Path, SHEET_ID
from send_excel import send


class Date(OperationExcel):

    def __init__(self,file):
        self.file = file
        super(Date, self).__init__()
        # self.file_name = file_name
        # super(Date, self).__init__()

    # def A(self):
    #     print 'wwwwwwww'
    def acquire_date(self,track_number):
        '''
        获取数据
        :return:
        '''

        url = "http://www.padtf.com/express-tracking.html"
        req = urllib2.Request(url)
        html = urllib2.urlopen(req).read()

        selector = etree.HTML(html)
        node_list = selector.xpath('''//*[@id="page"]/div[2]/div[3]/table[2]/tbody/tr[7]/td[4]/div/text()''')

        if not node_list:
            getstat = '未找到'

        else:
            getstat = node_list[0].xpath("./td[@class='style1']/span/strong/text()")
            if not getstat:
                getstat = node_list[0].xpath("./td[@class='style1']/span/text()")
            getstat = getstat[0].encode('utf-8').decode('utf-8')
        return track_number,getstat




# 这里传入一个Excel

# 返回值为指定列号的列数据,ssss是没用数据,无影响
lists = Date('ssss').get_col_all_data(col_number)
# 无用操作
file = Date('sss').A()

print len(lists)
list_data = []

i = 0
for list in lists:
    print(list)
    # 拿出列中的订单号发送请求返回运单号和状态,并追加到列表
    list_data.append(Date('sss').acquire_date(list))
    i = i+1
    if i > len(lists):
        break
    print i
# 把数据和文件名发送走
send(list_data,FILE_NAME)