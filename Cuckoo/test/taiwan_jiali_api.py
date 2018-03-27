# coding=utf8
<<<<<<< HEAD
import Queue
=======
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca
import re
import requests
import datetime
import sys
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')

<<<<<<< HEAD
a = Queue.Queue()
# www.timesoms.com
# url = "http://stg.timesoms.com/api/orders/40002002337"
url = "http://www.timesoms.com/api/orders/40002204411"
=======
# www.timesoms.com
# url = "http://stg.timesoms.com/api/orders/40002002337"
url = "http://www.timesoms.com/api/orders/40002002436"
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca
headers = {
    'Authorization': "Bearer sbv99QoVncfr4twUlpByLwGLNKMMfLlSKtU0DIZYGFl85o5SlWeMvsShlIvl"
}

res = requests.get(url, headers=headers).content
<<<<<<< HEAD
print res
=======
# print res
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca
all_data_obj = re.compile(r'"milestones":{(.*?)}', re.S)
all_data_list = all_data_obj.findall(res)
if all_data_list:

    data_info = all_data_list[0].split(',')
    for i in data_info:
        data_info_obj = re.compile(r'"(.*?)":"(.*?)"', re.S)
        status_info = data_info_obj.search(i)
        if status_info:
            logistics_time = status_info.groups()[1]
            status = status_info.groups()[0]
            print 'time:-------:', logistics_time
            print 'status:-------:', status
else:
    status = '未上线'
    logistics_time = ''
    # 以下2行测试使用******************************************************************
    print 'time:-------:', logistics_time
    print 'status:-------:', status