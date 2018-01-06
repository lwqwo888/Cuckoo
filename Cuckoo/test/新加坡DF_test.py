# coding=utf-8
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmmisTrack'
# url1 = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmsApiTrack&cno=080019639971'
# url2 = 'http://118.201.157.11/cgi-bin/GInfo.dll?MfcISAPICommand=EmsApiTrack'
url2 = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmsApiTrack&cno=080019173938&cp=936&ntype=101'

# params = {
#     'cno': '080019639971',
#     'ntype': '0',
# }
# res = requests.post(url, data=params)
res =  requests.get(url2).text
print res
with open("新加坡DF信息1.txt", "a") as f:
    f.write(res)