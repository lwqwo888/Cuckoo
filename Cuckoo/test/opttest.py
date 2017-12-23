# !/usr/bin/python
#-*- coding: utf-8 -*-
import getopt
import sys
import os
import threading
import time
import datetime
import urllib
import urllib2
from bs4 import BeautifulSoup
from lxml import etree
import requests
import re
# import ChangeIp
reload(sys)
sys.setdefaultencoding('utf-8')

# opts,args = getopt.getopt(sys.argv[1:],"hd:")
# print(type(opts))
# print(type(args))
# for o,v in opts:
#     if o in ('-d'):
#         db_name = v
#         print (db_name)
#     if o in ('-h'):
#         print("help")



# # lock_file = "lwq" + db_name
# # print(lock_file)
# # if os.path.exists(lock_file):
# #     print("cunzai")
# #     os.remove(lock_file)
# #     sys.exit(11111)
# # else:
# #     print("wu")
# # a = os.path.relpath(__file__)
# # b = os.path.split(a)
# # print("a--",a)
# # print("b--",b)
# # print(b[0])
# # current_path = os.path.split(os.path.relpath(__file__))[0]
# # print(current_path)
#
#
#
#
# # 建立不同线程的任务，事件的is_set()方法判断当前事件标志
# # 如果事件标志为False，执行wait()才会阻塞
# # 如果事件标志为Ture，则不会阻塞
# # event.set()方法可以将事件标志设置为Ture
# # event.clear()方法可以将事件标志设置为False
# def man(event):
#     if not event.is_set() :
#         print ("Hello Lancy, nice to meet you.")
#         event.wait()
#         print ("How about to watch a movie together?")
#     else:
#         event.clear()
#
# def woman(event):
#     if not event.is_set() :
#         print ("Hello Mike, today is a nice day!")
#         event.wait()
#         print ("Let's go!")
#     else:
#         event.clear()
#
# # 建立各种事件
# man_talk_event = threading.Event()
# woman_talk_event = threading.Event()
#
# # 创建线程,不同线程对应不同事件
# # 如果在start()之前设置t1.setDaemon(True)则不阻塞主线程，后台运行
# t1 = threading.Thread(target=man, args=(man_talk_event,), name='man')
# t2 = threading.Thread(target=woman, args=(woman_talk_event,), name='woman')
# # t1.setDaemon(True)
# # t2.setDaemon(True)
#
# # 启动线程，线程会阻塞在event.wait()那里，直到对应事件调用event.set()
# t1.start()
# time.sleep(1)
# t2.start()
# time.sleep(1)
#
# # 对应事件的set()方法将事件标志设置为True，则不阻塞线程
# # clear()将事件的标志设为False
# # 让man继续线程，并最后结束man线程
# man_talk_event.set()
# time.sleep(1)
# man_talk_event.clear()
#
# # 让woman继续线程，并最后结束woman线程
# woman_talk_event.set()
# time.sleep(1)
# woman_talk_event.clear()



# date_month = str(datetime.datetime.now().month)
# date_day = str(datetime.datetime.now().day)
# date_hour = datetime.datetime.now().hour
# filename = os.path.abspath(
#     '.') + os.sep + 'data' + os.sep + date_month + '_' + date_day + '_' + '07' + '.txt'
# print(filename)
#
#
# url = """http://www.t-cat.com.tw/Inquire/TraceDetail.aspx?BillID="571100024903"&ReturnUrl=Trace.aspx"""
#
# req = urllib2.Request(url)
# html = urllib2.urlopen(req).read()
#
# selector = etree.HTML(html)
# node_list = selector.xpath("//tr[@valign='center']")
#
# if not node_list:
#     getstat = '未找到'
#
# else:
#     getstat = node_list[0].xpath("./td[@class='style1']/span/strong/text()")
#     if not getstat:
#         getstat = node_list[0].xpath("./td[@class='style1']/span/text()")
#     getstat = getstat[0].encode('utf-8').decode('utf-8')
# print(getstat)


# bindIpObj = ChangeIp.bindIp()
# bindIpObj.randomIp()
# print '当前IP：%s  总IP：%s' % (str(bindIpObj.getIp()), str(bindIpObj.getIpsCount()))
# bindIpObj.changeIp(bindIpObj.getIp())
# proxy = {"http" : "mr_mao_hacker:sffqry9r@61.158.163.130:16816"}
#       "http://218.16.117.83:8033/APIQuery.aspx?TrackNum="
# url = "http://218.16.117.83:8033/APIQuery.aspx?TrackNum=571100034820"
# url = "http://www.padtf.com/express-tracking.html"
# header = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
#     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "Accept-Encoding":"gzip, deflate",
#     "Accept-Language":"zh-CN,zh;q=0.8",
#     "Cache-Control":"max-age=0",
#     "Connection":"keep-alive",
#     "Host":"218.16.117.83:8033",
#     "Upgrade-Insecure-Requests":"1",
# }
#
# formdata = {"seark": "571100025037",
#              "token": "",
#              "rec": "sekkform",
#              "originator": "",
#              "submin": "查询", }
# res = requests.post(url,data = formdata).text
# selector = etree.HTML(res)
# node_list = selector.xpath('''//*[@id="page"]/div[@class="content"]''')
# for i in node_list:
#     print i
# bindIpObj.changeIp("")
# res = requests.get(url).content.decode('gbk').encode('utf-8')
# pattern = re.compile(r'<scanstatusname>(.*?)</scanstatusname>', re.S)
# n = pattern.findall(res)
# status = n[len(n)-1]
# print status

# pattern = re.compile(r'<Route remark="(.*?)"', re.S)

# n = pattern.findall(res)
# print(type(n))
# if n == []:
#     print 66666666
# pattern = re.compile(r'accept_time="(.*?)"', re.S)
# t = pattern.findall(res)
# sf_list = [i for i in zip(n, t)]
# for i,j in sf_list:
#     status = i
#     time = j



# res_tab = r'<ishaspod>(.*?)</ishaspod>'
# stat = re.findall(res_tab, html, re.S | re.M)[0]

# res_tab1 = r'<scanstatusname>(.*?)</scanstatusname>'
# getstat_init = re.findall(res_tab1, html, re.S | re.M)
# i = 0
# print len(getstat_init)
# for x in range(len(getstat_init)):
#     getstat = re.findall(res_tab1, html, re.S | re.M)[i].decode('gbk')
#     res_tab2 = r'<scandate>(.*?)</scandate>'
#     date_list1 = re.findall(res_tab2, html, re.S | re.M)[i].decode('gbk')
#     res_tab3 = r'<scandime>(.*?)</scandime>'
#     date_list2 = re.findall(res_tab3, html, re.S | re.M)[i].decode('gbk')
#     logistics_time = date_list1 + ' ' + date_list2
    # tran_status = send_date(getstat, logistics_time, track, summary_status, '(51)',
    #                         '').acquire_date()




getstat = ''
url = "http://www.padtf.com/express-tracking.html"
formdata = {"seark": "571100030729",
            "token": "",
            "rec": "sekkform",
            "originator": "",
            "submin": "查询", }

res = requests.post(url, data=formdata).text
# print res
selector = etree.HTML(res)
node_list = selector.xpath('//td[@align="left"]')

if not node_list:
    getstat = '未找到'

else:
    i = node_list[-1]
    str = i.xpath('.//div[@align="left"]/text()')
    font = i.xpath('.//div[@align="left"]/font/text()')
    s = len(str)
    f = len(font)
    print s, f
    if s == 2 and f == 1:
        str_1 = i.xpath('.//div[@align="left"]/text()')[0].strip()
        str_2 = i.xpath('.//div[@align="left"]/text()')[1].strip()
        font_0 = i.xpath('.//div[@align="left"]/font/text()')[0].strip()
        getstat = str_1 + str_2 + font_0
    elif s == 3 and f == 2:
        str_1 = i.xpath('.//div[@align="left"]/text()')[1].strip()
        str_2 = i.xpath('.//div[@align="left"]/text()')[2].strip()
        font_0 = i.xpath('.//div[@align="left"]/font/text()')[0].strip()
        font_1 = i.xpath('.//div[@align="left"]/font/text()')[1].strip()
        getstat = font_0 + str_1 + font_1 + str_2
    else:
        getstat = i.xpath('.//div[@align="left"]/text()')[0].strip()
print getstat



