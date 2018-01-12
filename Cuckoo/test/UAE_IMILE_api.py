import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://47.52.205.72:8710/IMILEDianShangInterface/K9/getTrackingData.do'
params = {
    'type': 1,
    'code': '100000000432',
}
res = requests.post(url, data=params).content
print res
all_time = re.compile(r'', re.S)
all_status = re.compile(r'', re.S)
time_list = all_time.findall(res)
status_list = all_status.findall(res)