# coding=utf-8
import requests
import json
import re
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# url = 'http://www.sz56t.com:8082/selectTrack.htm?documentCode=1171226121221604271'
url = 'http://113.105.65.70:8032/query.aspx'
params = {
    'TrackNum': '114502789973',
    # 'Button1': '追踪',
}
json_data = requests.post(url, data=params).text

html = etree.HTML(json_data)

res_length = html.xpath('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText'][last()]/tr[@align="left"]''')
all_length = len(res_length)
print all_length

if all_length > 1:
    for i in range(all_length):
        i += 1
        num = str(i)
        status_list = html.xpath(('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText']
        [last()]/tr[@align="left"][%s]/td[4]/div/text()''')%num)
        # print status_list
        status = status_list[0].replace('\r', '').replace('\n', '').replace('\t', '').strip()
        time_list1 = html.xpath(('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText']
        [last()]/tr[@align="left"][%s]/td[1]/div/text()''')%num)
        time_list2 = html.xpath(('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText']
        [last()]/tr[@align="left"][%s]/td[2]/div/text()''')%num)
        logistics_time = time_list1[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '') + ' '\
                         + time_list2[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        with open("马来DF信息1.txt", "a") as f:
            f.write(logistics_time + '\n' + status + '\n')
else:
    status = '未上线'
    logistics_time = '未上线'
    # 以下2行测试使用******************************************************************
    with open("马来DF信息1.txt", "a") as f:
        f.write(logistics_time + '\n' + status + '\n')
