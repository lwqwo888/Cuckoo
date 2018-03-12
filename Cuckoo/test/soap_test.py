# coding=utf-8
from suds.client import Client

params={}
ClientInfo = {

        "AccountCountryCode": "HK",
        "AccountEntity"     : "HKG",
        "AccountNumber"     : "134289",
        "AccountPin"        : "321321",
        "UserName"          : "wangyuanhua@stosz.com",
        "Password"          : 'Bugo123456789*',
        "Version"           : "v1",
       # 'arr': '[31542390036]'
}
Shipments = {
    '31542390036','31542390036','31542390036','31542390036',
}
# params["Shipments"] = '31542390036'

params['ClientInfo'] = ClientInfo
params['Shipments'] = [Shipments, ]

# def websevice():
#     """
#     创建websevice请求
#     """
url = "https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?singleWsdl"
client = Client(url)
print client
# result = client.service
result = client.factory.create("ArrayOfString")
result.string = [ClientInfo, Shipments]
res = client.service.TrackShipments(result)
print res

# websev = websevice()
# ws = websev.service.TrackShipments(data)
# print ws