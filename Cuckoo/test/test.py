# coding=utf-8
from suds import WebFault
from suds.client import Client
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
str='G20-放假安排'
result = str.split('-')[1:][0]
print(result)
# 使用python调用webservice

url = 'http://webservice.webxml.com.cn/WebServices/WeatherWS.asmx?WSDL'
client = Client(url)
print (client)
print (client.service.getWeather('58367'))
