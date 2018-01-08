# coding=utf-8
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def control(key):
    status_err = key
    swtich = {
        'AT1': 'PickupInbound',
        'AT2': 'Processinginpickupbranch',
        'DT1': 'HubInbound',
        'DT2': 'HubOutbound',
        'AL1': 'BranchInboundinDeliveryBranch',
        'AL2': 'BranchOutboundinDeliveryBranch',
        'FD': 'SuccessfullyDelivered',
        'DF': 'DeliveryFailed',
        'RS': 'ReturnedtoShipper',
    }
    return swtich.get(key, status_err)

# url = 'http://uat.gdexapi.com/api/PreAlert/LatestDeliveryStatus/GdexCN/8715022643'
# url = 'http://uat.gdexapi.com/api/key/PreAlert/DeliveryStatus/8715022643'
url = 'https://www.gdexapi.com/api/key/PreAlert/DeliveryStatus/8715088314'# 8715025395  8715051450  8715023881
# url = 'http://uat.gdexapi.com/api/key/PreAlert/DeliveryStatus/4508815662'
# url = 'http://uat.gdexapi.com/api/key/PreAlert/DeliveryStatus/MY75002523704'
print url

params = {
    'ApiKey': 'vV9d4gBNZUiWxvX2Cn5P5ObzdxpCqMgIIzyFNWm7ZQY='
    }

api_data = requests.get(url, headers=params).content
print api_data
all_status_code = re.compile(r'"StatusCode":"(.*?)"', re.S)
all_time = re.compile(r'"StatusDateTime":"(.*?)"', re.S)
status_code_list = all_status_code.findall(api_data)
time_list = all_time.findall(api_data)
if time_list:
    gdex_list = [i for i in zip(status_code_list, time_list)]
    for status_code, logistics_time in gdex_list:
        status = status_code
        tran_status_label = control(status)
        # 以下2行测试使用******************************************************************
        print logistics_time + '\n' + status + '\n' + tran_status_label + '\n'
        with open("GDEX信息1.txt", "a") as f:
            f.write(logistics_time + '\n' + status + '\n' + tran_status_label + '\n')
else:
    status = '未找到'
    logistics_time = ''
    tran_status_label = status
    # 以下2行测试使用******************************************************************
    print logistics_time + '\n' + status + '\n' + tran_status_label + '\n'
    with open("GDEX信息1.txt", "a") as f:
        f.write(logistics_time + '\n' + status + '\n' + tran_status_label + '\n')
