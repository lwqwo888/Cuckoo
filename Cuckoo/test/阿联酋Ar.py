# coding=utf-8
import re
from suds.client import Client

# client_info = {
#         "AccountCountryCode": "HK",
#         "AccountEntity"     : "HKG",
#         "AccountNumber"     : "134289",
#         "AccountPin"        : "321321",
#         "UserName"          : "wangyuanhua@stosz.com",
#         "Password"          : 'Bugo123456789*',
#         "Version"           : "v1",
#        # 'arr': '[31542390036]'
# }
# shipments = [
#     '31542390036','31542390036','31542390036','31542390036',
# ]
# url = "https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?singleWsdl"
url = "http://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?singleWsdl"
# url = "https://ws.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc?wsdl"
# url = "https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?Wsdl"
client = Client(url)
client_info = client.factory.create("ClientInfo")
client_info.AccountCountryCode = "HK"
client_info.AccountEntity ="HKG"
client_info.AccountNumber = "134289"
client_info.AccountPin = "321321"
client_info.UserName = "wangyuanhua@stosz.com"
client_info.Password = 'Bugo123456789*'
client_info.Version = "v1"

shipments = client.factory.create("ns1:ArrayOfstring")
shipments.string = ['31542384705']

result = client.service
res = result.TrackShipments(ClientInfo=client_info, Shipments=shipments)
res_str = str(res)
obj_status = re.compile(r'UpdateDescription = "(.*?)"', re.S)
obj_time = re.compile(r'UpdateDateTime = (.*?)[A-Za-z]', re.S)
status_list = obj_status.findall(res_str)
time_list = obj_time.findall(res_str)
print time_list
if time_list:
    alianqiuAr_list = [x for x in zip(time_list, status_list)]
    for time, status in alianqiuAr_list:
        time_list = list(time.replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', ''))
        time_list.insert(10, ' ')
        logistics_time = ''.join(time_list)
        print logistics_time
        print status
else:
    status = '未上线'
    logistics_time = ''
    tran_status_label = status
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
    # 以下1行测试使用******************************************************************
    print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'
