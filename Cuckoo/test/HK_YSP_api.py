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
    # url = 'http://119.23.28.96/cgi-bin/GInfo.dll?EmsApiTrack&cno=' + track_number
    url = 'http://119.23.28.96/cgi-bin/GInfo.dll?EmsApiTrack&cno=789319545534'
    html = requests.get(url).content.decode('gbk').encode('utf-8')
    # print html
    all_status = re.compile(r'<INFO>(.*?)</INFO>', re.S)
    all_time = re.compile(r'<DATETIME>(.*?)</DATETIME>', re.S)
    status_list = all_status.findall(html)
    time_list = all_time.findall(html)

    if time_list:
        ysp_list = [i for i in zip(time_list, status_list)]
        for i, j in ysp_list:
            logistics_time = i + ' 00:00:00'
            ran_status_label = Control(str_process(j))
            # 以下2行测试使用******************************************************************
            with open("HK_YSP信息1.txt", "a") as f:
                f.write(logistics_time + '\n' + j + '\n' + '归类: ----------- :' + ran_status_label + '\n\n')
    else:
        get_stat = '未找到'
        get_time = '未找到'
        # 以下2行测试使用******************************************************************
        with open("HK_YSP信息1.txt", "a") as f:
            f.write(get_stat + '\n' + get_time + '\n')


def Control(original_str):
    print 'original_str : ',original_str
    # 派件
    if '正在派送途中' in original_str:
        ran_status = '正在派送途中'
    elif '快件在已装车准备发往'in original_str:
        ran_status = '正在派送途中'
    elif '快件在装车已发往'in original_str:
        ran_status = '正在派送途中'
    # 签收
    elif '快件到达' in original_str:
        ran_status = '快件到达'
    # 快件派送不成功
    elif '快件派送不成功' in original_str:
        ran_status = '快件派送不成功'
    # 其他官方未给出的状态
    else:
        ran_status = original_str
    return ran_status


def str_process(old_str):
    new_str = old_str.strip().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').lower()
    return new_str

acquire_date()