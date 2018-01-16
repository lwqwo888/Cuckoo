# coding=utf8
import re
import requests
import datetime
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://www.t-cat.com.tw/Inquire/Trace.aspx?no=620125438602'
html = requests.get(url).text
# print html
res = etree.HTML(html)
judge = res.xpath('''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td''')
length = len(judge)
print length
if length:
    i = 2
    while i <= 3:
        # xpath_str = '''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td[%s]//text()'''%str(i)
        if i == 2:
            xpath_str = '''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td[%s]//strong//text()''' % str(i)
            all_status = res.xpath(xpath_str)
            # print len(all_time)
            for j in all_status:
                # print len(j)
                print 'status:-------:', j.replace('\n', '').replace('\t', '').replace('\r', '').strip()
        elif i == 3:
            xpath_str = '''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td[%s]//span//text()''' % str(i)
            all_time = res.xpath(xpath_str)
            # print len(all_time)
            date_str = all_time[0].replace('\n', '').replace('\t', '').replace('\r', '').replace('/', '-').strip()
            time_str = all_time[1].replace('\n', '').replace('\t', '').replace('\r', '').strip()
            time = date_str + ' ' + time_str
            print 'time:--------:', time
        i += 1
else:
    print 'status:-------: 未上线'
    print 'time:--------: 未上线'