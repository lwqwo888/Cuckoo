# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import re
import requests

def acquire_date():
    '''
    获取数据
    :return:
    '''
    t = time.time()
    time_stamp = int(round(t * 10000))
    str_time = str(time_stamp)

    url = 'http://cdek-express.cn/ajax.php?JsHttpRequest=' + str_time + '-xml'+ '&Action=GetTrackingInfo&invoice=1171120061351709515'
    # url = 'http://cdek-express.cn/ajax.php?JsHttpRequest=' + str_time + '-xml'+ '&Action=GetTrackingInfo&invoice=' + track_number

    res = requests.get(url).content.decode('unicode_escape')
    # print res
    pattern = re.compile(r'"statusName":"(.*?)"', re.S)
    status_list = pattern.findall(res)
    pattern = re.compile(r'"date":"(.*?)"', re.S)
    datetime_list = pattern.findall(res)

    if len(status_list) == 0:
        getstat = '未找到'
        gettime = '未找到'
        # 以下2行测试使用******************************************************************
        with open("CDEK_eluosi信息1.txt", "a") as f:
            f.write(getstat + '\n' + gettime + '\n')
    else:
        CDEK_List = [i for i in zip(status_list, datetime_list)]
        for i,j in CDEK_List:
            getstat = i
            gettime = j.split('.')[::-1]
            gettime = gettime[0] + '-' + gettime[1] + '-' + gettime[2] + ' ' + '00:00:00'
            # 以下四行测试使用******************************************************************
            # print getstat
            # print gettime
            with open("CDEK_eluosi信息1.txt","a") as f:
                f.write(getstat +'\n'+ gettime + '\n')

acquire_date()
