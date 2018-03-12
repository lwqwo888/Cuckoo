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

def control_df(key):
    status_err = key
    swtich = {

        'AA': 'Access not allowed',
        'AB': 'Under investigation',
        'AC': 'Consignee Address Under Renovation',
        'AD': 'Consignee Payment Not Ready',
        'AE': 'Consignee Shifted',
        'AF': 'Customer Requests for Redirection',
        'AG': 'Customer Requests OC',
        'AH': 'Held Back In Office',
        'AI': 'Incomplete Consignee Address',
        'AJ': 'Late Linehaul Arrival',
        'AK': 'Misrouted Between Station',
        'AL': 'Missorted Between Route',
        'AM': 'No Such Address',
        'AN': 'Non Service Area (NSA)',
        'AP': 'Outskirt Delivery Area (ODA)',
        'AQ': 'Pending Custom Declaration',
        'AR': 'Refuse to Accept - Consignee Not In',
        'AS': 'Refuse to Accept - Damaged Shipment',
        'AT': 'Refuse to Accept - Delay Delivery',
        'AU': 'Refuse to Accept - Short Pieces',
        'AV': 'Refuse to Accept - No Such Order',
        'AW': 'Refuse to Accept - No Such Person',
        'AX': 'Refuse To Acknowledge  POD',
        'AY': 'Refuse To Acknowledge DO',
        'AZ': 'Sorry Card',
        'BA': 'Stop Delivery Instructed by HQ or Shipper',
        'BB': 'UTCD - Accident',
        'BC': 'UTCD - Criss Cross CN',
        'BD': 'UTCD - Heavy Rain',
        'BE': 'UTCD - Late Linehaul Arrival',
        'BF': 'UTCD - Natural Disaster',
        'BG': 'UTCD - Road Closed',
        'BH': 'UTCD - Vehicle Breakdown',
        'BI': 'Unable To Locate',
        'BJ': 'Refuse to Accept - Consignee Cancel Order',
        'BK': 'Hold for Reattempt Date',
        'RS': 'Returned to Shipper',
    }
    return swtich.get(key, status_err)

# url = 'http://uat.gdexapi.com/api/PreAlert/LatestDeliveryStatus/GdexCN/8715022643'
# url = 'http://uat.gdexapi.com/api/key/PreAlert/DeliveryStatus/8715022643'
# url = 'https://www.gdexapi.com/api/key/PreAlert/DeliveryStatus/8715088314'# 8720877432 8715025395  8715051450  8715023881  http://edi.gdexapi.com/
url = 'http://edi.gdexapi.com/api/key/PreAlert/DeliveryStatus/8715474246'
# url = 'http://uat.gdexapi.com/api/key/PreAlert/DeliveryStatus/4508815662'
# url = 'http://uat.gdexapi.com/api/key/PreAlert/DeliveryStatus/MY75002523704'
print url

params = {
            # 'vV9d4gBNZUiWxvX2Cn5P5ObzdxpCqMgIIzyFNWm7ZQY='
    'ApiKey': 'vV9d4gBNZUiWxvX2Cn5P5ObzdxpCqMgIIzyFNWm7ZQY='
    }

api_data = requests.get(url, headers=params).content
print api_data
all_status_code = re.compile(r'"StatusCode":"(.*?)"', re.S)
all_time = re.compile(r'"StatusDateTime":"(.*?)"', re.S)
all_df_code = re.compile(r'"ReasonCode":(.*?)}', re.S)
status_code_list = all_status_code.findall(api_data)
time_list = all_time.findall(api_data)
all_df_code_list = all_df_code.findall(api_data)
if time_list:
    gdex_list = [i for i in zip(status_code_list, all_df_code_list, time_list)]
    for status_code, df_code, logistics_time in gdex_list:
        if df_code != "null":
            # print type(df_code)
            df_code = df_code.replace('"', '')
            status = control_df(df_code)
            tran_status_label = df_code
        else:
            status = control(status_code)
            tran_status_label = status_code
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
