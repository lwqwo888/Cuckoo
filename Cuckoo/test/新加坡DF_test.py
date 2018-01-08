# coding=utf-8
import requests
from lxml import etree
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmmisTrack'
# url1 = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmsApiTrack&cno=080019639971'
# url2 = 'http://118.201.157.11/cgi-bin/GInfo.dll?MfcISAPICommand=EmsApiTrack'
url2 = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmsApiTrack&cno=080019173938&cp=936&ntype=101'
url3 = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmsApiTrack&cno=080019640276'

# params = {
#     'cno': '080019639971',
#     'ntype': '0',
# }
# res = requests.post(url, data=params)
res =  requests.get(url3).content.decode('gbk').encode("utf-8")
# print res

all_status = re.compile(r'<INFO>(.*?)</INFO>', re.S)
all_time = re.compile(r'<DATETIME>(.*?)</DATETIME>', re.S)
status_list = all_status.findall(res)
time_list = all_time.findall(res)

if time_list:
    ysp_list = [i for i in zip(time_list, status_list)]
    for i, j in ysp_list:
        if len(i) > 10:
            logistics_time = i + ':00'
        else:
            logistics_time = i + ' 00:00:00'
        status = j
        # tran_status_label = control(str_process(j))
        # 以下2行测试使用******************************************************************
        print logistics_time + '\n' + status + '\n'
else:
    status = '未找到'
    logistics_time = ''
    tran_status_label = status
    # 以下2行测试使用******************************************************************
    print logistics_time + '\n' + status + '\n' + tran_status_label + '\n'



with open("新加坡DF信息1.txt", "a") as f:
    f.write(res)