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
import requests
# import sys
# sys.path.append('../')
from lxml import etree

from operation_excel import OperationExcel
from config import FILE_NAME, col_number, FILE_Path, SHEET_ID
from send_excel import send
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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
        getstat = '未上线'
        url = 'http://www.t-cat.com.tw/Inquire/Trace.aspx?no=' + track_number
        html = requests.get(url).text
        # print html
        res = etree.HTML(html)
        judge = res.xpath(
            '''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td''')
        length = len(judge)
        # print length
        if length:
            i = 2
            while i <= 3:
                # xpath_str = '''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td[%s]//text()'''%str(i)
                if i == 2:
                    xpath_str = '''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td[%s]//strong//text()''' % str(
                        i)
                    all_status = res.xpath(xpath_str)
                    # print len(all_time)
                    for j in all_status:
                        # print len(j)
                        getstat =  j.replace('\n', '').replace('\t', '').replace('\r', '').strip()
                elif i == 3:
                    xpath_str = '''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td[%s]//span//text()''' % str(
                        i)
                    all_time = res.xpath(xpath_str)
                    # print len(all_time)
                    date_str = all_time[0].replace('\n', '').replace('\t', '').replace('\r', '').replace('/',
                                                                                                         '-').strip()
                    time_str = all_time[1].replace('\n', '').replace('\t', '').replace('\r', '').strip()
                    time = date_str + ' ' + time_str
                    # print 'time:--------:', time
                i += 1
        else:
            getstat = '未上线'

        return track_number,getstat




# 这里传入一个Excel

# 返回值为指定列号的列数据,ssss是没用数据,无影响
lists = Date('ssss').get_col_all_data(col_number)
# 无用操作
file = Date('sss').A()
length = len(lists)
list_data = []

i = 0
for list in lists:

    print "第%s个单号,共%s个: %s,"%(i,length,list)
    # 拿出列中的订单号发送请求返回运单号和状态,并追加到列表
    list_data.append(Date('sss').acquire_date(list))
    i = i+1
    if i > len(lists):
        break
    # print i
# 把数据和文件名发送走
send(list_data,FILE_NAME)


128510174121