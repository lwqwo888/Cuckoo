# coding=utf-8
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url = 'http://uat.gdexapi.com/api/PreAlert/LatestDeliveryStatus/GdexCN/8715022643'
# url = 'http://uat.gdexapi.com/api/PreAlert/DeliveryStatus/8106114656'
api_data = requests.get(url).content
print api_data