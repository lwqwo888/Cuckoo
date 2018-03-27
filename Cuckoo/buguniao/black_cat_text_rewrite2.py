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

from cat_date_text import send_date
def mian():
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

        # date_month = str(datetime.datetime.now().month)
        # date_day = str(datetime.datetime.now().day)
        # date_hour = datetime.datetime.now().hour
        #
        # if len(date_month) == 1:
        #     date_month = '0' + date_month
        # else:
        #     date_month = date_month
        # if len(date_day) == 1:
        #     date_day = '0' + date_day
        # else:
        #     date_day = date_day
        # if 7 < date_hour < 17:
        #     filename = os.path.abspath('.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '07' + '.txt'
        #     file_handler = open(filename.decode('utf-8'), 'wb')
        # elif 4 < date_hour < 7:
        #     filename = os.path.abspath('.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '04' + '.txt'
        #     file_handler = open(filename.decode('utf-8'), 'wb')
        # else:
        #     filename = os.path.abspath('.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '17' + '.txt'
        #     file_handler = open(filename.decode('utf-8'), 'a').write

        ftp = FTP()
        ftp.connect('61.57.227.35')
        ftp.login('cuc', 'c2017u10c18')

        print ftp.getwelcome()

        bufsize = 1024
        track = ''
        print 'nihao'
        # if 7 < date_hour < 17:
        #     filename = os.path.abspath(
        #         '.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '07' + '.txt'
        #     file_handler = open(filename.decode('utf-8'), 'a').write
        #
        #     ftp.retrbinary("RETR /Receive/cuc" + date_month + date_day + "07.SOD", file_handler, bufsize)
        # elif 4 < date_hour < 7:
        #     filename = os.path.abspath(
        #         '.') + os.sep + 'date' + os.sep + date_month + '_' + date_day + '_' + '04' + '.txt'
        #     file_handler = open(filename.decode('utf-8'), 'a').write
        #     ftp.retrbinary("RETR /Receive/cuc" + date_month + date_day + "04.NOD", file_handler, bufsize)
        # else:
        filename = os.path.abspath('.') + os.sep + 'date' + os.sep + '01' + '_' + '18' + '_' + '07' + '.txt'
        file_handler = open(filename.decode('utf-8'), 'a').write
        ftp.retrbinary("RETR /Receive/cuc" + '01' + '18' + "07.SOD", file_handler, bufsize)

        #filename = os.path.abspath('.') + os.sep + 'date' + os.sep + '12' + '_' + '21' + '_' + '17' + '.txt'
        with open(filename.decode('utf-8'), 'rb') as f:
            lines = f.readlines()
            count = len(lines)
        i = 0
        import math
        print count
        datas_line = []
        page_line = 1
        pagesize_line = 1000
        pagecount = int(math.ceil((float(count) / pagesize_line)));
        for line in lines:
            re_track = re.compile(r'(\d{5,20})\|(.*)')
            logistics_time = ''.join(line.replace("\r\n", "").split('|')[-5:-4])
            track = re.search(re_track, line).group(1)

            logistics_time = mix_commontime(logistics_time)
            status = line[line.replace("\r\n", "")[:-2].rfind("|") + 1:-1].replace('|', '').replace('\r', '').decode(
                "big5").strip().replace(' (PP)|', '')

            # send_date(status, logistics_time, track).insert_date_cat()
            datas_line.append((track, status, logistics_time))
            if len(datas_line) == 1000:
                send_date().insert_date_cat(datas_line)
                page_line += 1
                datas_line = []

            elif len(datas_line) < 1000:
                if (page_line == pagecount - 1) and (len(datas_line) == int(count % pagesize_line) - 1):
                    send_date().insert_date_cat(datas_line)
        print '%s --- %s' % (track, status)
        end_time = time.time()

        print '爬取结束共用时:' + str(end_time - start_time)
    except Exception, e:
        print e

        # 获取所有的数据
    select__final_datas = send_date().selete_delete_date()
    datas = []
    page = 1
    count = len(select__final_datas);
    pagesize = 500
    pagecount = int(math.ceil((float(count) / pagesize)));

    for select__final_data in select__final_datas:
        datas.append((str(select__final_data['id_shipping']), str(select__final_data['track_number']),
                      select__final_data['status_label'], str(select__final_data['date_at']),
                      select__final_data['status_label']))
        if len(datas) == 500:
            send_date().insert_date(datas)
            page += 1
            datas = []

        elif len(datas) < 500:
            if (page == pagecount - 1) and (len(datas) == int(count % pagesize) - 1):
                send_date().insert_date(datas)


if __name__ == '__main__':
    # 主函数
    start = time.time()
    mian()
    # 删除表中的数据
    send_date().delete_cat()
    end = time.time()
    print '爬虫用时{0}'.format(end - start)
