# coding=utf8
import re
import requests
import datetime
import sys
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')


def main():

    url = 'https://th.kerryexpress.com/th/track/?track=BJT1801031578'

    html = requests.get(url).text
    print html
    res = etree.HTML(html)
    judge = res.xpath('''/html/body/div[@class="sector-frame"]/div[@id="trackArea"]/div/div/div/div/div/div[2]/div[@class="status piority-success"]''')
    # print judge
    judge_len = len(judge)
    # print judge_len
    if judge_len:
        status_time_all = res.xpath(
            '''/html/body/div[@class="sector-frame"]/div[@id="trackArea"]/div/div/div/div/div/div[2]/div''')
        length = len(status_time_all)
        year_num = str(datetime.datetime.now().year)[:2]
        i = 1
        while i <= length:
            xpath_str = '''/html/body/div[@class="sector-frame"]/div[@id="trackArea"]/div/div/div/div/div/div[2]/div[%s]'''%str(i)
            time_list = res.xpath(xpath_str+'/div[@class="date"]//div//text()')
            status_list = res.xpath(xpath_str+'/div[@class="desc"]/div[@class="d1"]//text()')
            # print time_list
            # print status_list
            date_list = time_list[0][5:].split(' ')
            ascii_num = ord(time_list[1][5:][0][0])
            # print ascii_num
            if 58 > ascii_num > 47:
                time1 = time_list[1][5:] + ':00'
            else:
                time1 = '00:00:00'

            date_len = len(date_list)
            time_list1 = []
            if date_len > 2:
                date = date_list[2] + '-' + month_func(date_list[1].upper()) + '-' + date_list[0]
                t1 = year_num + date + ' ' + time1
                time_list1.append(t1)
            else:
                t1 = '00000000' + ' ' + time_list[1][5:]+':00'
                time_list1.append(t1)

            taiguo_jl_list = [x for x in zip(time_list1, status_list)]

            for logistics_time, status_str in taiguo_jl_list:
                status = status_str.replace('\n', '').replace('\t', '').replace('\r', '').strip()
                print 'time:-------:', logistics_time
                print 'status:-------:', status
                print '\n'
                with open("泰国嘉里信息1.txt", "a") as f:
                    f.write(logistics_time + '\n' + status + '\n')
            i += 1

    else:
        status = '未上线'
        logistics_time = '未上线'
        print 'time:-------:', logistics_time
        print 'status:-------:', status
        print '\n'
        with open("泰国嘉里信息1.txt", "a") as f:
            f.write(logistics_time + '\n' + status + '\n')

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

if __name__ == '__main__':
    main()