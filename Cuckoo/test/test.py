# 使用python调用webservice

from suds import WebFault
from suds.client import Client

url = 'http://webservice.webxml.com.cn/WebServices/WeatherWS.asmx?WSDL'
client = Client(url)
print (client)
print (client.service.getWeather('58367'))