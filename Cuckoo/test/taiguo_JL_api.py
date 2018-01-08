# coding=utf8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



url = 'http://exch.th.kerryexpress.com/ediwebapi_uat/SmartEDI/shipment_info'

res = requests.post(url).content