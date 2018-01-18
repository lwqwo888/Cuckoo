
# coding=utf-8
from suds.client import Client

# callService = {
#         "appToken": "604b2394a504b593ef2e806737ac9b06",
#         "appKey"     : "604b2394a504b593ef2e806737ac9b068674992310621bebc6e9326441dd4786",
#         "service"     : "getCargoTrack",
#         "paramsJson"        : "ALJAE7338000010YQ",
# }
# shipments = [
#     '31542390036','31542390036','31542390036','31542390036',
# ]

url = "http://tms.alljoylogistics.com/default/svc/wsdl"
client = Client(url)
print client

callService_info = client.factory.create("callService")
callService_info.appToken = "604b2394a504b593ef2e806737ac9b06"
callService_info.appKey ="604b2394a504b593ef2e806737ac9b068674992310621bebc6e9326441dd4786"
callService_info.service = "getCargoTrack"
callService_info.paramsJson = 'ALJAE7338000010YQ'


result = client.service
ws = result.callService(callService=callService_info)
print ws

result = client.service
ws = result.callService(appToken=callService_info)
print ws