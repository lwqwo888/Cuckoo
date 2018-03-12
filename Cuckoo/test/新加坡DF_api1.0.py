# coding=utf-8
import requests
from lxml import etree
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmsApiTrack&cno=' + result['track']


res =  requests.get(url).content.decode('gbk').encode("utf-8")
# print res

all_status = re.compile(r'<INFO>(.*?)</INFO>', re.S)
all_time = re.compile(r'<DATETIME>(.*?)</DATETIME>', re.S)
status_list = all_status.findall(res)
time_list = all_time.findall(res)
status_id = send_date(status, logistics_time, track, summary_status, '(252)', '').acquire_date_id()

if time_list:
    ysp_list = [i for i in zip(time_list, status_list)]
    for i, j in ysp_list:
        if len(i) > 10:
            logistics_time = i + ':00'
        else:
            logistics_time = i + ' 00:00:00'
        status = j
        tran_status_label = status
        # print logistics_time
        # print status
        # tran_status = send_date(status, logistics_time, track, summary_status, '(252)', '').acquire_date()
        # print tran_status
        # if tran_status:
        #     for tran_status_item in tran_status:
        #         if tran_status_item['status_label'].strip() in status:
        #             tran_status_label = tran_status_item['status_label']
        #             print tran_status_label
        #             break
        #         else:
        #             tran_status_label = status
        # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
        # 以下1行测试使用******************************************************************
        print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'

else:
    status = '未找到'
    logistics_time = ''
    tran_status_label = status
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
    # 以下1行测试使用******************************************************************
    print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'

