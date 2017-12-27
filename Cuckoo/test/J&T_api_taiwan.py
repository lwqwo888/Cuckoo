# coding=utf-8
# 此接口url地址为http/post类型地址
# xml信息请求报文
# 服务名:RouteService 语言为中文简体
# Head接入编码:BSPdevelop
# Body:请求内容
# passwd:密钥
# xml报文+密钥后进行md5和base64后即为校验码
# 构建post数据,内容为xml报文和校验码
# 发送post请求

import hashlib
import base64
import requests
import json
import re
import Queue
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    data_queue = Queue.Queue()
    url = "http://202.159.30.42:22223/jandt_web/szcuckoo/trackingAction!tracking.action"

    params = {
        "awb": "JK0000000010"
    }
    params = json.dumps(params,ensure_ascii=False)
    json_object = json.loads(params)
    res = requests.post(url,data=params).content.decode('unicode-escape')
    all_status = re.compile(r'"status":"(.*?)"', re.S)
    all_time = re.compile(r'"date_time":"(.*?)"', re.S)
    status_list = all_status.findall(res)
    datetime_list = all_time.findall(res)
    print "status",all_status
    if all_status == []:
        getstat = '未找到'
        gettime = '未找到'
    else:
        J_and_T_list = [i for i in zip(status_list, datetime_list)]
        for i, j in J_and_T_list:
            str_time = j.split(' ')
            time_list = str_time[0].split('-')[::-1]
            month_num = month_func(time_list[1])
            gettime = time_list[0] + '-' + month_num + '-' + time_list[2] + ' ' + str_time[1]
            print "gettime:   ", gettime
            print 'getstat:   ', i
        # print yinni_getstat
        # yinni_getstat = yinni_getstat.replace(' ', '').lower()
        # getstat = Control(yinni_getstat)
    # for i in getstat:
    #     with open("J&T信息1.txt","a") as f:
    #             f.write(i+'\n')

def Control(yn_str):
    # 派件
    if yn_str in str_process('Paket akan dikirim ke alamat penerima'):
        zh_str = '派件'
    # 签收
    elif yn_str in str_process('Paket telah diterima'):
        zh_str = '签收'
    # 收件 'Paket telah diterima oleh & 网点名称'
    elif yn_str in str_process('Paket telah diterima oleh & 网点名称'):
        note = yn_str.split('&')[1:][::1]
        zh_str = note + '收件'
    # 发件 'Paket akan dikirimkan ke & 网点名称':
    elif yn_str in str_process('Paket akan dikirimkan ke & 网点名称'):
        note = yn_str.split('&')[1:][::1]
        zh_str = note + '发件'
    # 到件 'Paket telah sampai di & 网点名称'
    elif yn_str in str_process('Paket telah sampai di & 网点名称'):
        note = yn_str.split('&')[1:][::1]
        zh_str = note + '到件'
    # 疑难件
    elif yn_str in str_process('Paket disimpan di gudang J&T'):
        zh_str = '疑难件'
    # 装袋
    elif yn_str in str_process('Pack'):
        zh_str = '装袋'
    # 拆袋
    elif yn_str in str_process('Unpack'):
        zh_str = '拆袋'
    # 快件将被退回
    elif yn_str in str_process('Paket akan diretur'):
        zh_str = '快件将被退回'
    # 快件处理中
    elif yn_str in str_process('Paket Gagal dipickup'):
        zh_str = '快件处理中'
    # 订单处理中
    elif yn_str in str_process('Manifes'):
        zh_str = '订单处理中'
    # 快件已被退回
    elif yn_str in str_process('Package returned to seller'):
        zh_str = '快件已被退回'
    # 运单无效
    elif yn_str in str_process('Expired AWB'):
        zh_str = '运单无效'
    # 其他官方未给出的状态
    else:
        zh_str = yn_str + ': J&T技术未给出此状态'
    return zh_str

# def month_func(str):
#     print '月份: ',str
#     if str == 'JAN':
#         month_num = '01'
#     elif str == 'FEB':
#         month_num = '02'
#     elif str == 'MAR':
#         month_num = '03'
#     elif str == 'APR':
#         month_num = '04'
#     elif str == 'MAY':
#         month_num = '05'
#     elif str == 'JUN':
#         month_num = '06'
#     elif str == 'JUL':
#         month_num = '07'
#     elif str == 'AUG':
#         month_num = '08'
#     elif str == 'SEP':
#         month_num = '09'
#     elif str == 'OCT':
#         month_num = '10'
#     elif str == 'NOV':
#         month_num = '11'
#     elif str == 'DEC':
#         month_num = '12'
#     else:
#         print '未知月份'
#     return month_num

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



def str_process(str):
    new_str = str.replace(' ', '').lower()
    return new_str

if __name__ == '__main__':
    main()


