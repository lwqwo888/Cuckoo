# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import re
import requests

def acquire_date():
    '''
    获取数据
    :return:
    '''
    t = time.time()
    time_stamp = int(round(t * 10000))
    str_time = str(time_stamp)

    url = 'http://cdek-express.cn/ajax.php?JsHttpRequest=' + str_time + '-xml'+ '&Action=GetTrackingInfo&invoice=1171120061351709515'
    # url = 'http://cdek-express.cn/ajax.php?JsHttpRequest=' + str_time + '-xml'+ '&Action=GetTrackingInfo&invoice=' + track_number

    res = requests.get(url).content.decode('unicode_escape')
    # print res
    pattern = re.compile(r'"statusName":"(.*?)"', re.S)
    status_list = pattern.findall(res)
    pattern = re.compile(r'"date":"(.*?)"', re.S)
    datetime_list = pattern.findall(res)

    if datetime_list:
        CDEK_List = [i for i in zip(status_list, datetime_list)]
        for status,j in CDEK_List:
            gettime = j.split('.')[::-1]
            logistics_time = gettime[0] + '-' + gettime[1] + '-' + gettime[2] + ' ' + '00:00:00'

            # tran_status = send_date(status, logistics_time, track, summary_status, '(198,200)', '').acquire_date()
            # if tran_status:
            #     for tran_status_item in tran_status:
            #         if tran_status_item['status_label'].strip() in status:
            #             tran_status_label = tran_status_item['status_label']
            #             break
            #         else:
            #             tran_status_label = status
            # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),
            #           tran_status_label).insert_date()
            # 以下3行测试使用******************************************************************
            print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'
            with open("CDEK_eluosi信息1.txt","a") as f:
                f.write(status + '\n' + logistics_time + '\n')

    else:
        status = '未找到'
        logistics_time = ''
        tran_status_label = status
        # 以下3行测试使用******************************************************************
        print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'
        with open("CDEK_eluosi信息1.txt", "a") as f:
            f.write(status + '\n' + logistics_time + '\n')

acquire_date()
