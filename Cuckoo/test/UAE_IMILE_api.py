# coding=utf-8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://47.52.205.72:8710/IMILEDianShangInterface/K9/getTrackingData.do'
params = {
    'type': 0,
    'code': '1000000006470',
}
res = requests.post(url, data=params).content
print res
all_time = re.compile(r'"time":"(.*?)"', re.S)
all_status = re.compile(r'"description":"(.*?)"', re.S)
time_list = all_time.findall(res)
status_list = all_status.findall(res)
imile_list = [x for x in zip(time_list, status_list)]
for logistics_time, status in imile_list:
    print logistics_time
    print status