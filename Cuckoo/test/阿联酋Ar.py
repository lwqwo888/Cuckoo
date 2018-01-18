# coding=utf-8
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

url = "https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?singleWsdl"
client = Client(url)
print client

client_info = client.factory.create("ClientInfo")
client_info.AccountCountryCode = "HK"
client_info.AccountEntity ="HKG"
client_info.AccountNumber = "134289"
client_info.AccountPin = "321321"
client_info.UserName = "wangyuanhua@stosz.com"
client_info.Password = 'Bugo123456789*'
client_info.Version = "v1"

shipments = client.factory.create("ns1:ArrayOfstring")
shipments.string = ['31542390036','31542390037','31542390038','31542390039']

result = client.service
ws = result.TrackShipments(ClientInfo=client_info, Shipments=shipments)
print ws