# coding=utf-8
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

<<<<<<< HEAD
url = 'http://47.52.146.142/podtrack/xml.aspx?hawb=66630768470'
=======
url = 'http://47.52.146.142/podtrack/xml.aspx?hawb=' + result['track']
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca

res = requests.get(url).content
# print res
all_date = re.compile(r'<action_DATE>(.*?)</action_DATE>', re.S)
all_time = re.compile(r'<action_TIME>(.*?)</action_TIME>', re.S)
all_status = re.compile(r'<STATUS>(.*?)</STATUS>', re.S)
date_list = all_date.findall(res)
time_list = all_time.findall(res)
status_list = all_status.findall(res)
<<<<<<< HEAD
# status_id = send_date(status, logistics_time, track, summary_status, '(222,224)', '').acquire_date_id()
if time_list:
    dex_list = [i for i in zip(date_list, time_list, status_list)]
    for date, time, status in dex_list:
        print date
        status = status.decode("gbk").encode("utf-8")
        date = date[:4] + "-" + date[4:6] + "-" + date[6:]
=======
status_id = send_date(status, logistics_time, track, summary_status, '(222,224)', '').acquire_date_id()
if time_list:
    dex_list = [i for i in zip(date_list, time_list, status_list)]
    for date, time, status in dex_list:
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca
        logistics_time = date + ' ' + time + ':00'
        # print logistics_time
        # print status
        # tran_status = send_date(status, logistics_time, track, summary_status, '(170)', '').acquire_date()
        # print tran_status
        # if tran_status:
        #     for tran_status_item in tran_status:
        #         if tran_status_item['status_label'].strip() in status:
        #             tran_status_label = tran_status_item['status_label']
        #             print tran_status_label
        #             break
        #         else:
        #             tran_status_label = status
<<<<<<< HEAD
        # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
        # 以下1行测试使用******************************************************************
        print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: '
=======
        send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
        # 以下1行测试使用******************************************************************
        print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca

else:
    status = '未找到'
    logistics_time = ''
    tran_status_label = status
    # print logistics_time
    # print status
<<<<<<< HEAD
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
=======
    send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca
    # 以下1行测试使用******************************************************************
    print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'
