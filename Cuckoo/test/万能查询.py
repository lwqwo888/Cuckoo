# coding=utf-8
# 免责声明: 此代码是为快捷查询由刘文强编写的,与服务器上其他工程师编写的泰国NIM(sync_NIM_final.py)代码稍有不同.
import re
import json
import time
import random
<<<<<<< HEAD
import urllib2
=======
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca
import datetime
import requests
import linecache
from lxml import etree
from dateutil.parser import parse
from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


<<<<<<< HEAD
def month_to_number(argument):
    switcher = {
        'Jan': "1",
        'Feb': "2",
        'Mar': "3",
        'Apr': "4",
        'May': '5',
        'Jun': '6',
        'Jul': '7',
        'Aug': '8',
        'Sep': '9',
        'Oct': '10',
        'Nov': "11",
        'Dec': '12'
    }
    return switcher.get(argument, "nothing")


s_time = time.time()
status_big_list = []
with open('万能查询运单号文档.txt', 'rb') as f:
    lines = f.readlines()

    for num in lines:

        url = "https://th.kerryexpress.com/en/track/?track=" + num
        html = requests.get(url).text
        # print html

        selector = etree.HTML(html)
        node_list = selector.xpath("//div[@class='col colStatus']/div")
        data = node_list[0].xpath("./div[@class='date']/div/text()")[0]
        # bindIpObj.changeIp('')

        if len(data) < 7:
            tran_status_label = '未上线'
            getstat = '未上线'
            logistics_time = ''
            print getstat
        else:
            i = 0
            for x in range(len(node_list)):
                getstat = node_list[i].xpath("./div/div[@class='d1']/text()")[0].strip().replace(' ', '')
                if "DeliverySuccessful" in getstat:
                    getstat = "DeliverySuccessful"
                print getstat
                date = node_list[i].xpath("./div[@class='date']/div/text()")
                year = "20" + date[0].replace(" ", "")[-2:]
                month = date[0].replace(" ", "")[-5:-2]
                month = month_to_number(month)
                day = date[0].replace(" ", "")[-7:-5]
                hour = date[1][-5:]
                logistics_time = year + '-' + month + '-' + day + ' ' + hour
                i += 1
                print logistics_time
=======
s_time = time.time()
status_big_list = []
with open('运单号文档.txt', 'rb') as f:
    lines = f.readlines()


    for num in lines:
        try:
            num = num.split()[0].replace('\n', '').replace('\r', '')
            url = 'http://stg.timesoms.com/api/orders/' + num
            headers = {
                "Authorization": "Bearer sbv99QoVncfr4twUlpByLwGLNKMMfLlSKtU0DIZYGFl85o5SlWeMvsShlIvl"
            }
            params = {
                'token': 'fJ83StsDzZPI50N0yksVUdaBVZIxR3FZqS4pKmG3yK2YQBVGQC0Pz7vNRuz0'
            }
            res = requests.get(url, headers=headers, params=params).text
            print res
            taiguo_keys = json.loads(res.text, object_pairs_hook=OrderedDict)['milestones'].keys()
            taiguo_values = json.loads(res.text, object_pairs_hook=OrderedDict)['milestones'].values()

            i = 0

            for taiguo_key in taiguo_keys:
                if not taiguo_values[i]:
                    taiguo_values[i] = ''
                i = i + 1
                info = "%s   *%s  %s" % (num, logistics_time, status)
                print info


            else:
                status = '未找到'
                logistics_time = ''
                tran_status_label = status
                # 以下2行测试使用******************************************************************
                print logistics_time + '\n' + status + '\n' + tran_status_label + '\n'

        except Exception as e:
            print (e)
        print '-'*60

>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca
e_time = time.time()
d_time = e_time - s_time
print '完成! 用时%s' % d_time



# for num in lines:
#     try:
#         num = num.split()[0].replace('\n', '').replace('\r', '')
#         # print len(num)
#         url = 'http://220.132.209.89/API/esp.php?A=esp&C=esp1234&S=' + num
#         res = requests.get(url).text
#         # print res
#         time_list = []
#         time_info = re.compile(r'"states_t":\[(.*?)\]', re.S)
#         status_info = re.compile(r'"states_s":\[(.*?)\]', re.S)
#         all_time = time_info.findall(res)
#         # status_id = send_date(status, logistics_time, track, '', '(258,262)','').acquire_date_id()
#
#         if all_time:
#             all_status = status_info.findall(res)
#             time_str = ''.join(all_time).split(',')
#             status_list = ''.join(all_status).split(',')
#
#             for i in time_str:
#                 list = i.replace('"', '').split(' ')
#                 date = list[0][:4] + '-' + list[0][4:6] + '-' + list[0][6:8]
#                 times = list[1][:2] + ':' + list[1][2:4] + ':' + list[1][4:6]
#                 time_list.append(date + ' ' + times)
#
#             taiwanysp_list = [x for x in zip(time_list, status_list)]
#             for logistics_time, status in taiwanysp_list:
#                 status = status.decode("unicode-escape").replace('"', '')
#             info = "%s   *%s  %s" % (num, logistics_time, status)
#             #     status_list.append(info)
#             # print status_list[-1]
#             print info
            # status_big_list.append(status_list[-1])
        # else:
        #     status = json.loads(res)["errorCode"]
        #     status1 = json.loads(res)["errorName"]
        #     info = '%s   *未上线  错误代码: %s 错误信息: %s ---------' % (num, status, status1)
        #     print info
            # status_big_list.append(info)

        # for new_status in status_big_list:
        #     print new_status
            # with open('泰国NIM.txt', 'a') as f:
            #     f.write(i + "\n")

    #
    #
    # except Exception as e:
    #     print (e)
e_time  = time.time()
d_time = e_time - s_time
print '完成! 用时%s' % d_time