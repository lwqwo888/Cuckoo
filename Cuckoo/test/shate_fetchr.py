# coding=utf-8
import requests
import json
import jsonpath
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''
34139383221567
3417600954322
34162221131171
34132013326895
34128202586915
34179902158930
34168242922516
34199406395696
34128887586872
34135351232641
34118953761970
'''

url = "https://api.fetchr.us/v3/tracking/history/34118953761970?reference_type=tracking_number"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImV4cCI6MTY1NTgxODUxNiwiaWF0IjoxNTAwMjk4NTE2fQ.eyJYLUNsaWVudC1OYW1lIjoiZHVtbXkiLCJzYW5kYm94IjpmYWxzZSwicHJpdmlsZWdlcyI6eyJjcmVkZW50aWFscyI6ImNydWQiLCJ0cmFja2luZyI6ImNydWQiLCJvcmRlcnMiOiJjcnVkIiwibm90aWZpY2F0aW9ucyI6ImNydWQifSwiWC1DbGllbnQtSUQiOjEzODYyODN9.G9LGvO-i-2X5YThioEepOTgY8GxRpkYp_sW-L8uz0I4'
}
res = requests.get(url, headers=headers).text
# print res
all_info_dict = json.loads(res)
all_time = jsonpath.jsonpath(all_info_dict, expr='$..tracking_information..status_date_local')
all_status = jsonpath.jsonpath(all_info_dict, expr='$..tracking_information..status_description')
if all_time:
    shate_fetchr_list = [x for x in zip(all_time, all_status)]
    for time, status in shate_fetchr_list:
        logistics_time = time
        tran_status_label = status
        print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'

else:
    status = '未上线'
    logistics_time = ''
    tran_status_label = status
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
    # 以下1行测试使用******************************************************************
    print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'
