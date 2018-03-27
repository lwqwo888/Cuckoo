# coding=utf8
import re
import requests
import datetime
import sys
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')

# 正式环境地址
url = "http://www.timesoms.com/api/orders/" + result['track']
headers = {
    # 正式环境headers
    'Authorization': "Bearer sbv99QoVncfr4twUlpByLwGLNKMMfLlSKtU0DIZYGFl85o5SlWeMvsShlIvl"
}

res = requests.get(url, headers=headers).content
# print res
all_data_obj = re.compile(r'"milestones":{(.*?)}', re.S)
all_data_list = all_data_obj.findall(res)
status_id = send_date(status, logistics_time, track, summary_status, '(164)', '').acquire_date_id()

if all_data_list:
    data_info = all_data_list[0].split(',')
    for i in data_info:
        data_info_obj = re.compile(r'"(.*?)":"(.*?)"', re.S)
        status_info = data_info_obj.search(i)
        if status_info:
            logistics_time = status_info.groups()[1]
            status = status_info.groups()[0]
            tran_status_label = status
            tran_status = send_date(status, logistics_time, track, summary_status, '(164)', '').acquire_date()
<<<<<<< HEAD
            # print tran_status
            # if tran_status:
            #     for tran_status_item in tran_status:
            #         if tran_status_item['status_label'].strip() in status:
            #             tran_status_label = tran_status_item['status_label']
            #             print tran_status_label
            #             break
            #         else:
            #             tran_status_label = status
=======
            print tran_status
            if tran_status:
                for tran_status_item in tran_status:
                    if tran_status_item['status_label'].strip() in status:
                        tran_status_label = tran_status_item['status_label']
                        print tran_status_label
                        break
                    else:
                        tran_status_label = status
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca
            # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
            # 以下2行测试使用******************************************************************
            print 'time:-------:', logistics_time
            print 'status:-------:', status

else:
    status = '未上线'
    logistics_time = ''
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
    # 以下2行测试使用******************************************************************
    print 'time:-------:', logistics_time
    print 'status:-------:', status