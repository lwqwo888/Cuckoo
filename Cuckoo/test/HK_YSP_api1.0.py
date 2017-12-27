# coding=utf8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def acquire_date():
    '''
    获取数据
    :return:
    '''
    # url = 'http://119.23.28.96/cgi-bin/GInfo.dll?EmsApiTrack&cno=789287474069'
    url = 'http://119.23.28.96/cgi-bin/GInfo.dll?EmsApiTrack&cno=' + track_number
    html = requests.get(url).content.decode('gbk').encode('utf-8')

    all_status = re.compile(r'<INFO>(.*?)</INFO>', re.S)
    all_time = re.compile(r'<DATETIME>(.*?)</DATETIME>', re.S)
    status_list = all_status.findall(html)
    time_list = all_time.findall(html)

    if status_list == []:
        getstat = '未找到'
        gettime = '未找到'
        # 以下2行测试使用******************************************************************
        with open("HK_YSP信息1.txt", "a") as f:
            f.write(getstat + '\n' + gettime + '\n')
    else:
        ysp_list = [i for i in zip(time_list, status_list)]
        for i, j in ysp_list:
            gettime = i + ' 00:00:00'
            getstat = j
            # 以下2行测试使用******************************************************************
            with open("HK_YSP信息1.txt", "a") as f:
                f.write(gettime + '\n' + getstat + '\n')

acquire_date()
