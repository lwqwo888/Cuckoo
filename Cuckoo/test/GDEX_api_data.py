# coding=utf-8
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# url = 'http://uat.gdexapi.com/api/PreAlert/LatestDeliveryStatus/GdexCN/8715022643'
# url = 'http://uat.gdexapi.com/api/key/PreAlert/DeliveryStatus/8715022643'
url = 'https://www.gdexapi.com/api/key/PreAlert/DeliveryStatus/8715051450'
# url = 'http://uat.gdexapi.com/api/key/PreAlert/DeliveryStatus/4508815662'
# url = 'http://uat.gdexapi.com/api/key/PreAlert/DeliveryStatus/MY75002523704'
print url

params = {
    'ApiKey': 'vV9d4gBNZUiWxvX2Cn5P5ObzdxpCqMgIIzyFNWm7ZQY='
    }

api_data = requests.get(url, headers=params).content
print api_data