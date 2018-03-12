# 1.1：接口名称：EmsApiTrack
# 1.2：接口参数：共3个
#      cno:运单号（长度7-30字符），默认查询顺序：内单号，转单号
#      ntype:语言等选择，默认:0,系统设置；100：强制中文；101：强制英文
#           +1000:（调整查询顺序：参考号，内单号，转单号）。
#           +10000:返回Json格式数据。
#      cp:语言编码,默认936,GBK；支持65001(utf-8)
# 1.3：返回数据：
# 返回值：第一行皆为状态行,
# 失败返回一个负数：-9:系统错误；-102：运单不存在。
# 成功返回100，后面为XML简易数据包装
# 100
# <EMS_INFO>
# <TDATE>取件日期时间</TDATE>
# <FROM>出发地</FROM>
# <DES>目的地</DES>
# <ITEM>件数</ITEM>
# <WEIGHT>重量</WEIGHT>
# <STATE>状态</STATE>
# <ADATE>签收日期时间</ADATE>
# <SIGN>签收人</SIGN>
# </EMS_INFO>
# <TRACK_DATA>
# <DATETIME>日期时间</DATETIME><PLACE>服务地点</PLACE><INFO>详细信息</INFO>
# ......
# </TRACK_DATA>
# <EXTRA_HEAD>
# 附加信息头
# </EXTRA_HEAD>
#
# 1.4：例子：
# 格式【1】: http://119.23.28.96/cgi-bin/GInfo.dll?EmsApiTrack&cno=1000000001
#
# 格式【2】: http://119.23.28.96/cgi-bin/GInfo.dll?MfcISAPICommand=EmsApiTrack&cno=1000000001
# '''


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
import re
import requests
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
        url = 'http://119.23.28.96/cgi-bin/GInfo.dll?EmsApiTrack&cno=' + track_number

        # print url
        res = requests.get(url).content.decode('gbk').encode('utf-8')
        print '66666'
        print type(res)
        print res

        pattern = re.compile(r'<INFO>(.*?)</INFO>', re.S)
        status = pattern.findall(res)

        if not status:
            getstat = '未找到'
        else:
            getstat = status

        return track_number,getstat

# 这里传入一个Excel

# 返回值为指定列号的列数据,ssss是没用数据,无影响
lists = Date('ssss').get_col_all_data(col_number)

# print len(lists)
# for i in lists:
#     print i
# 无用操作
file = Date('sss').A()
length = len(lists)
list_data = []

i = 1
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