<<<<<<< HEAD
# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
str='G20-放假安排'
result = str.split('-')[1:][0]
print(result)
=======
# 使用python调用webservice

from suds import WebFault
from suds.client import Client

url = 'http://webservice.webxml.com.cn/WebServices/WeatherWS.asmx?WSDL'
client = Client(url)
print (client)
print (client.service.getWeather('58367'))
>>>>>>> 75a0fcc1784506da036e6d9912e91fc22a383574
