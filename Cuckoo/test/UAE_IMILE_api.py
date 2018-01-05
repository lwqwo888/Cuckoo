import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://47.52.205.72:8710/IMILEDianShangInterface/K9/getTrackingData.do'
params = {
    'type': 1,
    'code': ''
}
res = requests.post(url, data=params).content
print res
