# coding=utf-8
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    url = "http://jk.jet.co.id:22261/jant_szcuckoo_web/szcuckoo/trackingAction!tracking.action"

    params = {
        "awb": track_number
    }
    params = json.dumps(params,ensure_ascii=False)
    json_object = json.loads(params)
    res = requests.post(url,data=params).content.decode('unicode-escape')
    all_status = re.compile(r'"status":"(.*?)"', re.S)
    all_time = re.compile(r'"date_time":"(.*?)"', re.S)
    status_list = all_status.findall(res)
    datetime_list = all_time.findall(res)

    if datetime_list:
        J_and_T_list = [i for i in zip(status_list, datetime_list)]
        for status, j in J_and_T_list:
            str_time = j.split(' ')
            time_list = str_time[0].split('-')[::-1]
            month_num = month_func(time_list[1])
            logistics_time = time_list[0] + '-' + month_num + '-' + time_list[2] + ' ' + str_time[1]
            # 以下四行测试使用******************************************************************
            # print logistics_time
            # print status
    else:
        status = '未找到'
        logistics_time = '未找到'
        # 以下2行测试使用******************************************************************
        # print logistics_time
        # print status

def month_func(mth):
    swtich = {
        'JAN': '01',
        'FEB': '02',
        'MAR': '03',
        'APR': '04',
        'MAY': '05',
        'JUN': '06',
        'JUL': '07',
        'AUG': '08',
        'SEP': '09',
        'OCT': '10',
        'NOV': '11',
        'DEC': '12',
    }
    return swtich.get(mth, '00')


if __name__ == '__main__':
    main()


