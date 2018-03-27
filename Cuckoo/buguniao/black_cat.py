#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : black_cat.py
# @Author: handan
# @Date  : 2017/10/19
# @Desc  :
#
from ftplib import FTP
import time
import sys
import os
import re
import datetime


from cat_date import send_date

reload(sys)
from dateutil.parser import parse

def mix_commontime(t):
    '''
    :param t:输入你想要的解析的文件格式
    :return:
    '''
    return parse(t).strftime('%Y-%m-%d %H:%M:%S')

sys.setdefaultencoding('utf-8')

summary_status    = ''
status            = ''
logistics_time    = ''
tran_status_label = ''
try:
    start_time = time.time()
    # bindIpObj= ChangeIp.bindIp()
    # bindIpObj. randomIp()
    # print '当前IP：%s  总IP：%s' % (str(bindIpObj.getIp()),str(bindIpObj.getIpsCount()))
    # bindIpObj. changeIp(bindIpObj.getIp())

    date_month = str(datetime.datetime.now().month)
    date_day = str(datetime.datetime.now().day)
    date_hour = datetime.datetime.now().hour

    if len(date_month) == 1:
        date_month = '0' + date_month
    else:
        date_month = date_month
    if len(date_day) == 1:
        date_day = '0' + date_day
    else:
        date_day = date_day
    if 7 < date_hour < 17:
        filename = os.path.abspath('.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '07' + '.txt'
        file_handler = open(filename.decode('utf-8'), 'wb')
    elif 4 < date_hour < 7:
        filename = os.path.abspath('.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '04' + '.txt'
        file_handler = open(filename.decode('utf-8'), 'wb')
    else:
        filename = os.path.abspath('.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '17' + '.txt'
        file_handler = open(filename.decode('utf-8'), 'a').write

    ftp = FTP()
    ftp.connect('61.57.227.35')
    ftp.login('cuc', 'c2017u10c18')

    print ftp.getwelcome()

    bufsize = 1024

    print 'nihao'
    if 7 < date_hour < 17:
        print 'okkkkkkkkkkkkkkkkkk'
        filename = os.path.abspath(
            '.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '07' + '.txt'
        file_handler = open(filename.decode('utf-8'), 'a').write

        print '22222222222222222222222222222222222222'
        ftp.retrbinary("RETR /Receive/cuc" + date_month + date_day + "07.SOD", file_handler, bufsize)
        print '333333333333333333333'
    elif 4 < date_hour < 7:
        filename = os.path.abspath(
            '.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '04' + '.txt'
        file_handler = open(filename.decode('utf-8'), 'a').write
        ftp.retrbinary("RETR /Receive/cuc" + date_month + date_day + "04.NOD", file_handler, bufsize)
    else:
        filename = os.path.abspath('.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '17' + '.txt'
        file_handler = open(filename.decode('utf-8'), 'a').write
        ftp.retrbinary("RETR /Receive/cuc" + date_month + date_day + "17.SOD", file_handler, bufsize)
    # filename = os.path.abspath('.')+os.sep+'date'+os.sep+'10'+'_'+'20'+'_'+'07'+'.txt'

    print 'okkkkkkkkkkkkkkkkkkk'
    with open(filename.decode('utf-8'), 'rb') as f:
        lines = f.readlines()
    # bindIpObj.changeIp('')
    for line in lines:
        re_track = re.compile(r'(\d{5,20})\|(.*)')
        logistics_time = ''.join(line.replace("\r\n", "").split('|')[-5:-4])
        track = re.search(re_track, line).group(1)

        # status_id = send_date(status, logistics_time, track, ' ', '(27)', '').acquire_date_id()
        # if status_id:
        # print status_id
        logistics_time = mix_commontime(logistics_time)
        status = line[line.replace("\r\n", "")[:-2].rfind("|") + 1:-1].replace('|', '').replace('\r', '').decode("big5").strip().replace(' (PP)|', '')
        print logistics_time
        # tran_status = send_date(status, logistics_time, track, summary_status, '(27)', '').acquire_date()

        send_date(status, logistics_time, track, '', '', '').insert_date_cat()

    select__final_datas = send_date('', '', '', '', '', '').selete_delete_date()

    for select__final_data in select__final_datas:
        send_date(select__final_data['status_label'], str(select__final_data['date_at']), str(select__final_data['track_number']), ' ', str(select__final_data['id_shipping']), select__final_data['status_label']).insert_date()

        # if tran_status:
        #     for tran_status_item in tran_status:
        #         if tran_status_item['status_label'].strip() in status:
        #             tran_status_label = tran_status_item['status_label']
        #
        #             break
        #         else:
        #             tran_status_label = status
        #     send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
        # else:
        #     pass
    print '%s --- %s' % (track,status)
    end_time = time.time()

    print '爬取结束共用时:'+str(end_time-start_time)
except Exception,e:
    print e
