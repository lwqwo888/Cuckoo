# coding=utf-8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://47.52.205.72:8710/IMILEDianShangInterface/K9/getTrackingData.do'
params = {
    'type': 0,
    'code': result['track'],
}
res = requests.post(url, data=params).content
print res
all_time = re.compile(r'"time":"(.*?)"', re.S)
all_status = re.compile(r'"description":"(.*?)"', re.S)
time_list = all_time.findall(res)
status_list = all_status.findall(res)
# status_id = send_date(status, logistics_time, track, '', '(260)','').acquire_date_id()
if time_list:
    imile_list = [x for x in zip(time_list, status_list)]
    for logistics_time, status in imile_list:
        tran_status_label = status
        # print logistics_time
        # print status
        # tran_status = send_date(status, logistics_time, track, summary_status, '(260)', '').acquire_date()
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

        with open('阿联酋IM信息.txt', 'a') as f:
            f.write(logistics_time + '\n' + status + '\n')

else:
    status = '未上线'
    logistics_time = '未上线'
    tran_status_label = status
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
    # 以下1行测试使用******************************************************************
    print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'


