# coding=utf-8
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url = 'http://113.105.65.70:8032/query.aspx'
params = {
    'TrackNum': result['track'],
    # 'Button1': '追踪',
}
json_data = requests.post(url, data=params).text
html = etree.HTML(json_data)
res_length = html.xpath('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText'][last()]/tr[@align="left"]''')
all_length = len(res_length)
status_id = send_date(status, logistics_time, track, summary_status, '(244)', '').acquire_date_id()
if all_length > 1:
    for i in range(all_length):
        i += 1
        num = str(i)
        status_list = html.xpath(('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText'][last()]/
        tr[@align="left"][%s]/td[4]/div/text()''')%num)
        status = status_list[0].replace('\r', '').replace('\n', '').replace('\t', '').strip()
        time_list1 = html.xpath(('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText'][last()]/
        tr[@align="left"][%s]/td[1]/div/text()''')%num)
        time_list2 = html.xpath(('''//html/body/form[@id='form1']/center/div/table[@class='HtmlText'][last()]/
        tr[@align="left"][%s]/td[2]/div/text()''')%num)
        logistics_time = time_list1[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '') + ' '\
                         + time_list2[0].replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
        tran_status_label = status
        # print logistics_time
        # print status
        # tran_status = send_date(status, logistics_time, track, summary_status, '(244)', '').acquire_date()
        # print tran_status
        # if tran_status:
        #     for tran_status_item in tran_status:
        #         if tran_status_item['status_label'].strip() in status:
        #             tran_status_label = tran_status_item['status_label']
        #             print tran_status_label
        #             break
        #         else:
        #             tran_status_label = status
        # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
        # 以下1行测试使用******************************************************************
        print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'

else:
    status = '未找到'
    logistics_time = ''
    tran_status_label = status
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
    # 以下1行测试使用******************************************************************
    print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'

