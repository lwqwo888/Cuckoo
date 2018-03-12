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
import json
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
        # 测试接口
        url = "http://202.159.30.42:22223/jandt_web/szcuckoo/trackingAction!tracking.action"
        # url = "http://jk.jet.co.id:22261/jant_szcuckoo_web/szcuckoo/trackingAction!tracking.action"

        params = {
            "awb": track_number
        }
        params = json.dumps(params, ensure_ascii=False)
        json_object = json.loads(params)

        res = requests.post(url, data=params).content.decode('unicode-escape')
        pattern = re.compile(r'"status":"(.*?)"', re.S)
        status = pattern.findall(res)
        if status == []:
            getstat = '未找到'

        else:
            yinni_getstat = status[-1]
            yinni_getstat = yinni_getstat.replace(' ', '').lower()
            getstat = self.Control(yinni_getstat)

        return track_number,getstat

    def Control(self,yn_str):
        # 派件
        if yn_str in self.str_process('Paket akan dikirim ke alamat penerima'):
            zh_str = '派件'
        # 签收
        elif yn_str in self.str_process('Paket telah diterima'):
            zh_str = '签收'
        # 收件 'Paket telah diterima oleh & 网点名称'
        elif yn_str in self.str_process('Paket telah diterima oleh & 网点名称'):
            note = yn_str.split('&')[1:][::1]
            zh_str = note + '收件'
        # 发件 'Paket akan dikirimkan ke & 网点名称':
        elif yn_str in self.str_process('Paket akan dikirimkan ke & 网点名称'):
            note = yn_str.split('&')[1:][::1]
            zh_str = note + '发件'
        # 到件 'Paket telah sampai di & 网点名称'
        elif yn_str in self.str_process('Paket telah sampai di & 网点名称'):
            note = yn_str.split('&')[1:][::1]
            zh_str = note + '到件'
        # 疑难件
        elif yn_str in self.str_process('Paket disimpan di gudang J&T'):
            zh_str = '疑难件'
        # 装袋
        elif yn_str in self.str_process('Pack'):
            zh_str = '装袋'
        # 拆袋
        elif yn_str in self.str_process('Unpack'):
            zh_str = '拆袋'
        # 快件将被退回
        elif yn_str in self.str_process('Paket akan diretur'):
            zh_str = '快件将被退回'
        # 快件处理中
        elif yn_str in self.str_process('Paket Gagal dipickup'):
            zh_str = '快件处理中'
        # 订单处理中
        elif yn_str in self.str_process('Manifes'):
            zh_str = '订单处理中'
        # 快件已被退回
        elif yn_str in self.str_process('Package returned to seller'):
            zh_str = '快件已被退回'
        # 运单无效
        elif yn_str in self.str_process('Expired AWB'):
            zh_str = '运单无效'
        # 其他官方未给出的状态
        else:
            zh_str = yn_str + ': J&T技术未给出此状态'
        return zh_str

    def str_process(self,str):
        new_str = str.replace(' ', '').lower()
        return new_str

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