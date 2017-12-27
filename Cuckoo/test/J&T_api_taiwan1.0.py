# coding=utf-8
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    url = "http://202.159.30.42:22223/jandt_web/szcuckoo/trackingAction!tracking.action"

    params = {
        # "awb": "JK0000000010"
        "awb": track_number
    }
    params = json.dumps(params,ensure_ascii=False)
    json_object = json.loads(params)
    res = requests.post(url,data=params).content.decode('unicode-escape')
    all_status = re.compile(r'"status":"(.*?)"', re.S)
    all_time = re.compile(r'"date_time":"(.*?)"', re.S)
    status_list = all_status.findall(res)
    datetime_list = all_time.findall(res)
    getstat = '未找到'
    gettime = '未找到'
    if status_list == []:
        getstat = getstat
        gettime = gettime
        # 以下2行测试使用******************************************************************
        with open("J&T信息1.txt","a") as f:
                f.write(gettime+'\n'+getstat+'\n')
    else:
        J_and_T_list = [i for i in zip(status_list, datetime_list)]
        for i, j in J_and_T_list:
            str_time = j.split(' ')
            time_list = str_time[0].split('-')[::-1]
            month_num = month_func(time_list[1])
            gettime = time_list[0] + '-' + month_num + '-' + time_list[2] + ' ' + str_time[1]
            # 以下四行测试使用******************************************************************
            gettime = gettime
            getstat = i
            with open("J&T信息1.txt","a") as f:
                    f.write(gettime+'\n'+getstat+'\n')

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


