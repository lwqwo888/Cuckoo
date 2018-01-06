# coding=utf8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://exch.th.kerryexpress.com/ediwebapi/SmartEDI/shipment_info'
params = {
    'app_id': '{Integration information – app_id}',
    'app_key': '{Integration information – app_key}'
    }
res = requests.post(url, data=params).content