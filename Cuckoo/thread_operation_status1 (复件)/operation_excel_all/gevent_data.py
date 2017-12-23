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
import requests
import Queue

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Date(OperationExcel):

    def __init__(self,file=None):
        self.file = file
        self.data_queue = Queue.Queue()
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
        print 'okkkkkkkkkkkkkkkkkkkkkkk'
        getstat = ''
        url = "http://www.padtf.com/express-tracking.html"
        formdata = {"seark": track_number,
                    "token": "",
                    "rec": "sekkform",
                    "originator": "",
                    "submin": "查询", }

        res = requests.post(url, data=formdata).text
        # print res
        selector = etree.HTML(res)
        node_list = selector.xpath('//td[@align="left"]')
        list_data = []
        if not node_list:
            getstat = '未找到'

        else:
            i = node_list[-1]
            str = i.xpath('.//div[@align="left"]/text()')
            font = i.xpath('.//div[@align="left"]/font/text()')
            s = len(str)
            f = len(font)
            # print s, f
            if s == 2 and f == 1:
                str_1 = i.xpath('.//div[@align="left"]/text()')[0].strip()
                str_2 = i.xpath('.//div[@align="left"]/text()')[1].strip()
                font_0 = i.xpath('.//div[@align="left"]/font/text()')[0].strip()
                getstat = str_1 + str_2 + font_0
            elif s == 3 and f == 2:
                str_1 = i.xpath('.//div[@align="left"]/text()')[1].strip()
                str_2 = i.xpath('.//div[@align="left"]/text()')[2].strip()
                font_0 = i.xpath('.//div[@align="left"]/font/text()')[0].strip()
                font_1 = i.xpath('.//div[@align="left"]/font/text()')[1].strip()
                getstat = font_0 + str_1 + font_1 + str_2
            print getstat
            self.data_queue.put(track_number + "\t" + getstat)
            # while not self.data_queue.empty():
            #     print 8888888888
            print self.data_queue.get()


    def main(self):
        self.acquire_date('43r3443')
        print self.data_queue.get()


# i = 1
# for list in lists:
#     print "第%s个单号,共%s个: %s," % (i, length, list)
#     # 拿出列中的订单号发送请求返回运单号和状态,并追加到列表
#     list_data.append(Date('sss').acquire_date(list))
#     i = i+1
#     if i > len(lists):
#         break
# 把数据和文件名发送走
# send(list_data,FILE_NAME)
if __name__ == '__main__':
    Date().main()