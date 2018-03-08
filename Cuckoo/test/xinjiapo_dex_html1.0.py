# coding=utf-8
import requests
from lxml import etree
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# url = 'http://47.52.146.142/podtrack/xml.aspx?hawb=' + result['track']
url = "https://cds.roadbull.com/order/track/RB_DEX66630719993"

res = requests.get(url).content
# print res
print "*"*80

html = etree.HTML(res)
list = html.xpath('''/html/body/div[@class="body_bg"]//div[@id="tracking"]/div/div/div/div[1]/div/ul//li/span''')
xpath_str1 = '''/html/body/div[@class="body_bg"]//div[@id="tracking"]/div/div/div/div[1]/div/ul//li/span[]//text()''' % str(i+1)
status_list = html.xpath(xpath_str1)

length = len(list)
i = 0
while i < length:
    xpath_str2 = '''/html/body/div[@class="body_bg"]//div[@id="tracking"]/div/div/div/div[1]/div/ul/li[%s]/p//text()''' % str(i+1)
    time_list = html.xpath(xpath_str2)
    print time_list[0].split('/')
    i += 1
# for i in list:
#     print i.replace('\n', '').replace('\t', '').replace('\r', '').strip()


# status_id = send_date(status, logistics_time, track, summary_status, '(222,224)', '').acquire_date_id()
# if time_list:
#     dex_list = [i for i in zip(date_list, time_list, status_list)]
#     for date, time, status in dex_list:
#         logistics_time = date + ' ' + time + ':00'
#         # print logistics_time
#         # print status
#         # tran_status = send_date(status, logistics_time, track, summary_status, '(170)', '').acquire_date()
#         # print tran_status
#         # if tran_status:
#         #     for tran_status_item in tran_status:
#         #         if tran_status_item['status_label'].strip() in status:
#         #             tran_status_label = tran_status_item['status_label']
#         #             print tran_status_label
#         #             break
#         #         else:
#         #             tran_status_label = status
#         # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
#         # 以下1行测试使用******************************************************************
#         print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', \
#             tran_status_label + '\n'
#
# else:
#     status = '未找到'
#     logistics_time = ''
#     tran_status_label = status
#     # print logistics_time
#     # print status
#     # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
#     # 以下1行测试使用******************************************************************
#     print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ',\
#         tran_status_label + '\n'
