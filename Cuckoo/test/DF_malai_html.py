# coding=utf-8
import requests
import datetime
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://etrace.9625taqbin.com/gli_trace/GDXTX010S10Action_doSearch.action'
params = {
    'jvCd':'42dec70a4f25166d',
    # 'sTimeDifference':'671cb6bcdedd72c7',
    # 'sSelectedLanguage':'73f9a3a3f2cf56bc',
    # 'sCountryCd':'0968983fa1feb763',
    # 'sLanguageMode':'0',
    'CHAR_SET':'3f572693955bb3ff',
    # 'sDefCharSet':'3f572693955bb3ff',
    # 'sCharSetCsv':'3f572693955bb3ff',
    # 'action%3AGDXTX010S10Action_doSearch':'Track',
    'tTrackingNoInputVal1': '114502605943',
    'tTrackingNoInputVal2': '',
    'tTrackingNoInputVal3': '',
    'tTrackingNoInputVal4': '',
    'tTrackingNoInputVal5': '',
    'tTrackingNoInputVal6': '',
    'tTrackingNoInputVal7': '',
    'tTrackingNoInputVal8': '',
    'tTrackingNoInputVal9': '',
    'tTrackingNoInputVal10': '',
}

year = datetime.datetime.now().year
month = datetime.datetime.now().month
res = requests.post(url, data=params).content
# print res
html = etree.HTML(res)
res1 = html.xpath('/html/body/form[@id="GDXTX010S10Action_doSearch"]/div[@align="center"]/table[@class="meisai"]//tr')
length = len(res1)
print length
if length != 0:
    i = 1
    while i <= length:
        xpath_str1 = '''/html/body/form[@id="GDXTX010S10Action_doSearch"]/div[@align="center"]/table[@class="meisai"]//tr[%s]/td[1]/text()'''%str(i)
        xpath_str2 = '''/html/body/form[@id="GDXTX010S10Action_doSearch"]/div[@align="center"]/table[@class="meisai"]//tr[%s]/td[2]/text()'''%str(i)
        xpath_str3 = '''/html/body/form[@id="GDXTX010S10Action_doSearch"]/div[@align="center"]/table[@class="meisai"]//tr[%s]/td[3]/text()'''%str(i)
        status_list = html.xpath(xpath_str1)
        date_list = html.xpath(xpath_str2)
        time_list = html.xpath(xpath_str3)
        malai_df_list = [j for j in zip(date_list, time_list, status_list)]
        for date_str, time_str, status_str in malai_df_list:
            date = date_str.replace('\n', '').replace('\t', '').replace('\r', '').strip()
            time = time_str.replace('\n', '').replace('\t', '').replace('\r', '').strip()
            status = status_str.replace('\n', '').replace('\t', '').replace('\r', '').strip()
            month_num = int(date[:2])
            if month_num > month:
                new_year = year - 1
            else:
                new_year = year
            logistics_time = str(new_year) + '-' + date + ' ' + time
            logistics_time = str(year) + '-' + date + ' ' + time
            print logistics_time
            print status
            with open("马来DF信息1.txt", "a") as f:
                f.write(logistics_time + '\n' + status + '\n')
        i += 1

else:
    status = '未上线'
    logistics_time = ''
    tran_status_label = status
    # 以下2行测试使用******************************************************************
    print logistics_time + '\n' + status + '\n' + tran_status_label + '\n'
    with open("马来DF信息1.txt", "a") as f:
        f.write(logistics_time + '\n' + status + '\n')