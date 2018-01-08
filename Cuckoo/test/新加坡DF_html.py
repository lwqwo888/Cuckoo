# coding=utf-8
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmmisTrack'
url1 = 'http://118.201.157.11/cgi-bin/GInfo.dll?EmsApiTrack&'
url2 = 'http://118.201.157.11/cgi-bin/GInfo.dll?MfcISAPICommand=EmsApiTrack'
params = {
    # 'w': 'sgatoz',
    # 'cmodel': '',
    'cno': '080019640276',
    'ntype': '0',
    # 'cp': '65001'
}
res = requests.post(url, data=params).text
print res
html = etree.HTML(res)

tr_label_amount = html.xpath('''//html/body/div[@id='defaultContent']//table[@class='trackListTable']//div[@id='oDetail']//tr''')
length = len(tr_label_amount)
# print length
if length > 1:
    num = 2
    while num <= length:
        td_label_amount = html.xpath('''//html/body/div[@id='defaultContent']//table[@class='trackListTable']//div[@id='oDetail']//tr[''' + str(num) + ']//td''')
        td_label_len = len(td_label_amount)
        td_label_len += 1
        all_time_str = '''//html/body/div[@id='defaultContent']//table[@class='trackListTable']//div[@id='oDetail']//tr[last()]//td[1]/text()'''
        all_status_str = '''//html/body/div[@id='defaultContent']//table[@class='trackListTable']//div[@id='oDetail']//tr[last()]//td[3]/text()'''
        logistics_time = html.xpath(all_time_str)[0] + ':00'
        status = html.xpath(all_status_str)[0]

        num += 1
        print logistics_time
        print status

else:
    logistics_time = ''
    status = '未找到'
    tran_status_label = status
    print logistics_time
    print status




















    # i = 1
    # while i < length1:
    #     if i == 2:
    #         i += 1
    #     all_data_str = '''//html/body/div[@id='defaultContent']//table[@class='trackListTable']//div[@id='oDetail']//tr[last()]//td[''' + str(i) + ']/text()'
    #     print html.xpath(all_data_str)[0]
    #     i += 1