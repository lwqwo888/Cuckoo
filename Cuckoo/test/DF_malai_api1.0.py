# coding=utf-8
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url = 'http://113.105.65.70:8032/query.aspx'
params = {
    '__VIEWSTATE': '/wEPDwUKMTg2MTYyMDc5M2RkjCDPEC/ksTqq44KYqvtadq7XLC4=',
    '__EVENTVALIDATION': '/wEWAwKi0rjlDwKvgcuQCQKM54rGBuq0mYrzxG6dbfcTTEtuhzTz4r+/',
    'TrackNum': track_number,
    'Button1': '追踪',
}
json_data = requests.post(url, data=params).text

html = etree.HTML(json_data)

res_length = html.xpath('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText'][last()]/tr[@align="left"]''')
all_length = len(res_length)

if all_length > 1:
    for i in range(all_length):
        i += 1
        num = str(i)
        status_list = html.xpath(('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText'][last()]/tr[@align="left"][%s]/td[4]/div/text()''')%num)
        status = status_list[0].replace('\r', '').replace('\n', '').replace('\t', '').strip()
        time_list1 = html.xpath(('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText'][last()]/tr[@align="left"][%s]/td[1]/div/text()''')%num)
        time_list2 = html.xpath(('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText'][last()]/tr[@align="left"][%s]/td[2]/div/text()''')%num)
        logistics_time = time_list1[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '') + ' '\
                         + time_list2[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        print logistics_time
        print status
else:
    status = '未上线'
    logistics_time = '未上线'
    # 以下2行测试使用******************************************************************
    print logistics_time
    print status
