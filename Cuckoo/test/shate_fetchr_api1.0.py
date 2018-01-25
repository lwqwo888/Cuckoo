# coding=utf-8
import requests
import json
import jsonpath
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url = "https://api.fetchr.us/v3/tracking/history/" + result['track'] + "?reference_type=tracking_number"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImV4cCI6MTY1NTgxODUxNiwiaWF0IjoxNTAwMjk4NTE2fQ.eyJYLUNsaWVudC1OYW1lIjoiZHVtbXkiLCJzYW5kYm94IjpmYWxzZSwicHJpdmlsZWdlcyI6eyJjcmVkZW50aWFscyI6ImNydWQiLCJ0cmFja2luZyI6ImNydWQiLCJvcmRlcnMiOiJjcnVkIiwibm90aWZpY2F0aW9ucyI6ImNydWQifSwiWC1DbGllbnQtSUQiOjEzODYyODN9.G9LGvO-i-2X5YThioEepOTgY8GxRpkYp_sW-L8uz0I4'
}
res = requests.get(url, headers=headers).text
# print res
all_info_dict = json.loads(res)
all_time = jsonpath.jsonpath(all_info_dict, expr='$..tracking_information..status_date_local')
all_status = jsonpath.jsonpath(all_info_dict, expr='$..tracking_information..status_description')
# status_id = send_date(status, logistics_time, track, '', '(274)','').acquire_date_id()
if all_time:
    shate_fetchr_list = [x for x in zip(all_time, all_status)]
    for time, status in shate_fetchr_list:
        logistics_time = time
        tran_status_label = status
        # print logistics_time
        # print status
        # tran_status = send_date(status, logistics_time, track, summary_status, '(274)', '').acquire_date()
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
    status = '未上线'
    logistics_time = ''
    tran_status_label = status
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
    # 以下1行测试使用******************************************************************
    print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'
