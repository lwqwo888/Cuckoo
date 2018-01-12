# coding=utf8
import re
import requests
import datetime
import sys
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://www.t-cat.com.tw/Inquire/Trace.aspx?no=620083192784'
html = requests.get(url).text
# print html
res = etree.HTML(html)
# judge = res.xpath('''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td''')
# length = len(judge)
i = 3
while i <= 4:
    xpath_str = '''/html/body/form[@id="form1"]/div[@id="wrapper"]/div[@id="contentContainer"]//div[@id="main"]/div[@class="contentsArea"]//div[@id="ContentPlaceHolder1_tblResult"]//table[@class="tablelist"]//tr[last()]/td[%s]//text()'''%str(i)
    if i == 3:
        all_time = res.xpath(xpath_str)
        print len(all_time)
        for j in all_time:
            print len(j)
            print 'time:--------:',j.replace('\n', '').replace('\t', '').replace('\r', '').strip()
    elif i == 4:
        all_status = res.xpath(xpath_str)
        # print len(all_time)
        for j in all_status:
            print len(j)
            print 'status:-------:',j.replace('\n', '').replace('\t', '').replace('\r', '').strip()
    i += 1
